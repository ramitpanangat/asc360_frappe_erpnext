import frappe
from frappe import get_doc, _

no_cache = 1

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer = get_doc("Customer", username.full_name).as_dict()

    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if customer.customer_group == "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict
    filters = {}

    if len(form_d)>0:
        if form_d["name"] != "":
            filters["name"] = form_d["name"]
        if form_d["scope_of_policy"] != "":
            filters["scope_of_policy"] = form_d["scope_of_policy"]

    plan_master = frappe.get_all("Customised Policy", filters=filters, fields=["*"])
    product_map = frappe.get_all("Operator Product Mapping", filters={"operator":username.full_name}, fields=["*"])
    plan_list = []
    for plan in plan_master:
        for cust in product_map:
            if plan.name == cust.policy:
                plan_list.append(plan)

    policy_master = frappe.get_meta("Customised Policy")

    scope_of_policy = policy_master.get_field("scope_of_policy").options.split("\n")


    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.plan_master = plan_list
    context.scope_of_policy = scope_of_policy
    context.params = form_d