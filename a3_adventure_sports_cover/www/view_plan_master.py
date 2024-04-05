import frappe
from frappe import get_doc

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
        
    plan_master = get_doc("Customised Policy",frappe.form_dict.docname)
    username = get_doc("User", frappe.session.user)
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    context.plan_master = plan_master
    context.insurance_plan_details = plan_master.insurance_plan_details
    context.policy_premium = plan_master.policy_premium
    context.activities = plan_master.activity_list