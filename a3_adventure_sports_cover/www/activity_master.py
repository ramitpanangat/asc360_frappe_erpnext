from erpnext.setup.doctype import territory
import frappe
from frappe import get_doc, get_value, _


no_cache = 1

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if customer_group == "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)


    form_d = frappe.form_dict
    filters = {"operator": username.full_name}

    if len(form_d)>0:
        #Filter with Activity Name
        if form_d["name"] != "":
            filters["name"] = form_d["name"]
        if form_d["activity_level"] != "":
            filters["activity_level"] = form_d["activity_level"]
        if form_d["activity_category"] != "":
            filters["activity_category"] = form_d["activity_category"]
        if form_d["territory"] != "":
            filters["activity_territory"] = form_d["territory"]
            
    activities = frappe.get_all("Operator Activity",filters=filters, fields=["*"])
    all_activities = frappe.get_all("Operator Activity",filters={"operator": username.full_name}, fields=["*"])
    levels = frappe.get_all("Activity Levels", fields=["*"])
    categories = frappe.get_all("Activity Category", fields=["*"])
    territories = frappe.get_all("Territory", fields=["*"])
    
    print(form_d)
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image
    
    context.param = form_d
    context.activities = activities
    context.all_activities = all_activities
    context.levels = levels
    context.categories = categories
    context.territories = territories