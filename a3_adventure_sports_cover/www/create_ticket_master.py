import frappe
from frappe import get_doc, get_value, _

no_cache = 1

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if customer_group == "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image
    context.username = username.full_name