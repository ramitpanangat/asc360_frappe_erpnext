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
    if customer_group != "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    operators = get_doc("Operator", frappe.form_dict.docname)


    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.operators = operators
    context.username = username.full_name
    context.user_type = customer_group