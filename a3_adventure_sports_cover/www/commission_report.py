import frappe
from frappe import get_doc, get_list, get_value, _

no_cache = 1

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")
    form_d = frappe.form_dict
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    filters={"operator": username.full_name}


    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    page = 0
    if len(form_d)>0:
        if "status" in form_d:
            filters["status"] = form_d["status"]
        
        if "page" not in form_d or int(form_d["page"]) == 1:
            page = 0
        else:
            page = (int(form_d["page"]) * 10) - 10

    commission_report = get_list("Operator Commission Payable", filters=filters, fields=["*"], limit_start=page, limit_page_length=10)
    commission_report_meta = frappe.get_meta("Operator Commission Payable").fields
    status_ = [meta for meta in commission_report_meta if meta.label=="Status"]
    status_options = status_[0].options.split("\n")

    context.commission_report = commission_report
    context.user_type = customer_group
    context.statuses = status_options
    context.params = form_d
    print(form_d)
    next_data = get_list("Operator Commission Payable", filters=filters, limit_start=(((int(form_d["page"])+1) * 10) - 10) if page>0 else 0, limit_page_length=10)
    if "page" not in form_d:
        context.next_page = 2 if len(next_data)>0 else 0
        context.prev_page = 0
    else:
        if int(form_d["page"]) == 0:
            context.next_page = int(form_d['page']) + 2 if len(next_data)>0 else 0
        else:
            context.next_page = int(form_d['page']) + 1 if len(next_data)>0 else 0

        if int(form_d["page"]) == 1:
            context.prev_page = 0
        else:
            context.prev_page = int(form_d["page"]) - 1