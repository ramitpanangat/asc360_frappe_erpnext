import frappe
from frappe import get_doc, _
from datetime import datetime, timedelta

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    username = get_doc("User", frappe.session.user)
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    invoice = get_doc("Sales Invoice",frappe.form_dict.docname)
    d = {"days": invoice.posting_time.days}
    d["hours"], rem = divmod(invoice.posting_time.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    context.invoice = invoice
    context.posting_time = "{hours}:{minutes}:{seconds}".format(**d)
    context.items = invoice.items
