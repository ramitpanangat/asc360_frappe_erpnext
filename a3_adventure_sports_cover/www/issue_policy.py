import frappe
from frappe import get_doc, get_value, _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict
    
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if customer_group == "Agent Customer":
        filters = {"agent_name": username.full_name, "docstatus": 1, "policy_type": "Single Policy", "pdf_added": "Completed"}
    else:
        filters = {"operator": username.full_name, "docstatus": 1, "policy_type": "Single Policy", "pdf_added": "Completed"}

    for key in form_d:
        if key != 'page':
            if form_d[key] != "":
                filters[key] = form_d[key]

    page = 0
    if len(form_d)>0:
        if "page" not in form_d or int(form_d["page"]) == 1:
            page = 0
        else:
            page = (int(form_d["page"]) * 10) - 10
    
    policy_issue = frappe.get_all("B2B Policy Issue", filters=filters, fields=["*"], limit_start=page, limit_page_length=10)


    if customer_group == "Agent Customer":
        all_policy_issue = frappe.get_all("B2B Policy Issue", filters={"agent_name": username.full_name, "docstatus": 1, "policy_type": "Single Policy"}, fields=["*"])
    else:
        all_policy_issue = frappe.get_all("B2B Policy Issue", filters={"operator": username.full_name, "docstatus": 1, "policy_type": "Single Policy"}, fields=["*"])

    customer_list = set()
    for issue in all_policy_issue:
        if customer_group == "Agent Customer":
            if issue.agent_name==username.full_name:
                customer_list.add(issue.customer_name)
        else:
            if issue.operator==username.full_name:
                customer_list.add(issue.customer_name)
    
    policies_issued = []
    for policy in policy_issue:
        if customer_group == "Agent Customer":
            if policy.agent_name==username.full_name:
                policies_issued.append(policy)
        else:
            if policy.operator==username.full_name:
                policies_issued.append(policy)

    items = frappe.get_all("Item", fields=["*"])

    item_list = set()
    for item in items:
        for pol in policies_issued:
            if item.item_code == pol.policy:
                if item.parent_policy==pol.policy_name:
                    item_list.add(item.item_code)

    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.policy_issue = policies_issued
    context.all_policy_issue = all_policy_issue
    context.customers = customer_list
    context.policies = item_list
    context.params = form_d
    context.user_type = customer_group
    if "page" not in form_d:
        context.next_page = 2
        context.prev_page = 0
    else:
        if int(form_d["page"]) == 0:
            context.next_page = int(form_d['page']) + 2
        else:
            next_data = frappe.get_all("B2B Policy Issue", filters=filters, limit_start=(((int(form_d["page"])+1) * 10) - 10), limit_page_length=10)
            context.next_page = int(form_d['page']) + 1 if len(next_data) else 0

        if int(form_d["page"]) == 1:
            context.prev_page = 0
        else:
            context.prev_page = int(form_d["page"]) - 1