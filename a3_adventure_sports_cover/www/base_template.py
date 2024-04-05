from ast import operator
import frappe
from frappe import cache_manager
import frappe.www.list
from frappe import _, get_doc
import datetime


no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    email = frappe.session.user
    username = get_doc("User", frappe.session.user)
    customer = get_doc("Customer", username.full_name).as_dict()

    context.userData = frappe.session
    context.user_type = customer.customer_group


