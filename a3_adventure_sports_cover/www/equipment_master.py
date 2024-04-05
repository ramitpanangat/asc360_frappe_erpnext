import frappe
from frappe import get_doc, get_value, _


no_cache = 1


def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User": # Change to != Website user
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if customer_group == "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    
    form_d = frappe.form_dict

    filters = {"operator": username.full_name}

    if len(form_d)>0:
        # Filter with Equipment Type
        if form_d["equipment_type"] != "":
            filters["equipment_type"] = form_d["equipment_type"]
        
    equipments = frappe.get_all("Operator Equipment", filters=filters, fields=["*"])

    context.username = username.full_name
    print("Photo idar hai", username.user_image)
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image

    context.equipments = equipments
    context.params = form_d