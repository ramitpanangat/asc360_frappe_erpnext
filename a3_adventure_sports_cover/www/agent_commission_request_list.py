import frappe
from frappe import get_doc, get_value, _

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if customer_group != "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict
    filters = {"agent":username.full_name, "docstatus":1}

    if len(form_d)>0:
        #Filter with Name
        if form_d["name"] != "":
            filters["name"] = form_d["name"]
  
    commission_payment = frappe.get_all("Agent Commission Payment", filters=filters, fields=["*"])
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image
    

    context.params = form_d
    context.user_type = customer_group
    context.commission_payment_list = commission_payment