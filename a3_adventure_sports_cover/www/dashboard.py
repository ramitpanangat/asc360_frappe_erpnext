from ast import operator
from erpnext.erpnext_integrations.connectors.shopify_connection import get_url
import frappe
import frappe.www.list
from html2text import html2text
from frappe import _, get_doc
from csv import DictReader
from pandas import read_csv, ExcelFile
from frappe.utils.file_manager import save_file, save_file_on_filesystem

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    username = get_doc("User", frappe.session.user)
    customer = get_doc("Customer", username.full_name).as_dict()
    form_d = frappe.form_dict
    if len(form_d)>0:
        if not form_d["page"] or int(form_d["page"]) == 1:
            page = 0
        else:
            page = (int(form_d["page"]) * 10) - 10
    else:
        page = 0
    if customer.customer_group == "Agent Customer":
        policy_issued = frappe.get_all("B2B Policy Issue", filters={"agent_name": username.full_name, "docstatus": 1, "pdf_added": "Completed", "policy_type":"Single Policy"}, fields=["*"], limit_start=page, limit_page_length=10)
        all_policy_issued = frappe.get_all("B2B Policy Issue", filters={"agent_name": username.full_name, "docstatus": 1}, fields=["*"])
        commission_payable = frappe.get_all("Agent Commission Payable", filters={"agent": username.full_name}, fields=["*"])
        user_details = get_doc("Agents", username.full_name)

    else:
        policy_issued = frappe.get_all("B2B Policy Issue", filters={"operator": username.full_name, "docstatus": 1, "pdf_added": "Completed", "policy_type":"Single Policy"}, fields=["*"], limit_start=page, limit_page_length=10)
        all_policy_issued = frappe.get_all("B2B Policy Issue", filters={"operator": username.full_name, "docstatus": 1}, fields=["*"])
        commission_payable = frappe.get_all("Operator Commission Payable", filters={"operator": username.full_name}, fields=["*"])
        user_details = get_doc("Operator", username.full_name)

        context.ATOAI_member = user_details.atoai_member
        context.ministry_of_tourism = user_details.registered_with_ministry_of_tourism
        context.registered_with_state_tourism = user_details.registered_with_state_tourism

    context.userData = frappe.session
    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    
    if customer.primary_address:
        context.address = html2text(customer.primary_address)
    else:
        context.address = customer.territory
    
    if username.birth_date:
        context.birth_date = username.birth_date.strftime("%d-%m-%Y")
    else:
        context.birth_date = "N/A"
    context.gender = username.gender
    context.policy_issue = policy_issued

    number_of_policy = 0
    for pol in all_policy_issued:
        if customer.customer_group == "Agent Customer":
            if pol.agent_name==username.full_name:
                number_of_policy += 1
        else:
            if pol.operator==username.full_name:
                number_of_policy += 1
    context.no_issue = number_of_policy
    
    total_issuance_amount = 0
    for issued in policy_issued:
        if customer.customer_group == "Agent Customer":
            if issued.agent_name == username.full_name:
                total_issuance_amount += issued.amount
        else:
            if issued.operator == username.full_name:
                total_issuance_amount += issued.amount

    context.total_issuance_amount = "{:.2f}".format(round(total_issuance_amount, 2))

    operator_commission_amount = 0
    for commission in commission_payable:
        if commission.operator==username.full_name:
            operator_commission_amount += commission.commission_payable

    operator_credit_balance = frappe.get_value("Operator Balance", username.full_name, "balance_available")
    context.operator_commission_amount = "{:.2f}".format(round(operator_commission_amount, 2))
    if operator_credit_balance:
        context.operator_credit_balance = "{:.2f}".format(round(operator_credit_balance, 2))
    else:
        context.operator_credit_balance = "{:.2f}".format(round(0, 2))
    context.user_type = customer.customer_group
    if "page" not in form_d:
        context.next_page = 2
        context.prev_page = 0
    else:
        if int(form_d["page"]) == 0:
            context.next_page = int(form_d['page']) + 2
        else:
            if customer.customer_group == "Agent Customer":
                next_data = frappe.get_all("B2B Policy Issue", filters={"agent_name": username.full_name, "docstatus": 1, "pdf_added": "Completed", "policy_type":"Single Policy"}, limit_start=(((int(form_d["page"])+1) * 10) - 10), limit_page_length=10)
            else:
                next_data = frappe.get_all("B2B Policy Issue", filters={"operator": username.full_name, "docstatus": 1, "pdf_added": "Completed", "policy_type":"Single Policy"}, limit_start=(((int(form_d["page"])+1) * 10) - 10), limit_page_length=10)
            context.next_page = int(form_d['page']) + 1 if len(next_data)>0 else 0

        if int(form_d["page"]) == 1:
            context.prev_page = 0
        else:
            context.prev_page = int(form_d["page"]) - 1

    ###############################################################
    
    # xls = ExcelFile('http://adventure.sports.cover:8021/files/bulk_customer_data.xls')
    # df = xls.parse(xls.sheet_names[0]).to_dict()
    # for i in range(len(df["Customer Name"])):
    #     print(f"Customer: ", df["Customer Name"][i])
    #     print(f"Gender: ", df["Gender"][i])
    #     print(f"Email: ", df["Email ID"][i])
    # data = save_file_on_filesystem(fname="bulk_customer_data.xls", content="/home/acube/Downloads/bulk_customer_data.xls", is_private=0)