from erpnext.erpnext_integrations.connectors.shopify_connection import get_url
import frappe
from frappe import get_doc, _
from html2text import html2text

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    booking = get_doc("Issue",frappe.form_dict.docname)

    username = get_doc("User", frappe.session.user)
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    context.booking = booking
    context.description = html2text(booking.description)