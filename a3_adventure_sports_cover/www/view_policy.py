import frappe
from frappe import get_doc, _

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    invoices = frappe.db.sql(""" SELECT * FROM `tabSales Invoice`; """, as_dict=True)
    invoices_child = frappe.db.sql(""" SELECT * FROM `tabSales Invoice Item`; """, as_dict=True)
    username = get_doc("User", frappe.session.user)
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    context.invoices = invoices
    for i in invoices_child:
        print(f"\n\n\n\n\n\n\n{i}\n\n\n\n\n\n\n\n\n")