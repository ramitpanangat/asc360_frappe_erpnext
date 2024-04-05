from ast import operator
import frappe
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
    customer = get_doc("Customer", username.full_name)
    profile = f"/{frappe.get_value('File', {'attached_to_name':'arjun@test.com'},['file_url'])}"
    photo = username.user_image
    operator_details = get_doc("Operator", username.full_name)

    context.userData = frappe.session
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image
    context.address = customer.primary_address
    context.ATOAI_member = operator_details.atoai_member
    context.ministry_of_tourism = operator_details.registered_with_ministry_of_tourism
    context.registered_with_state_tourism = operator_details.registered_with_state_tourism
    context.birth_date = username.birth_date.strftime("%d-%m-%Y")
    context.gender = username.gender
    context.photo = photo 
    context.mode_of_business = operator_details.mode_of_business
    context.territory = operator_details.territory
    context.mobile = username.mobile_no 
    context.email = email 
 