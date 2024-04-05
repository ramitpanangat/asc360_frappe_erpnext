from dataclasses import fields
import frappe
from frappe import get_doc, get_value, _

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if customer_group == "Agent Customer":
        filters = {"agent": username.full_name}
    else:
        filters = {"operator":username.full_name}

    for key in form_d:
        if key != 'page':
            if form_d[key] != "":
                filters[key] = form_d[key]
    
    if len(form_d)>0:
        if not form_d["page"] or int(form_d["page"]) == 1:
            invoice_list = frappe.get_all("Sales Invoice", filters=filters, fields=["*"], limit_start=0, limit_page_length=10)
        else:
            page = (int(form_d["page"]) * 10) - 10
            invoice_list = frappe.get_all("Sales Invoice", filters=filters, fields=["*"], limit_start=page, limit_page_length=10)
    else:
        invoice_list = frappe.get_all("Sales Invoice", filters=filters, fields=["*"], limit_start=0, limit_page_length=10)
        
    
    if customer_group == "Agent Customer":
        suggest_invoices = frappe.get_all("Sales Invoice", filters={"agent" : username.full_name}, fields=["*"])
        invoices = frappe.get_all("Sales Invoice", filters={"agent" : username.full_name}, fields=["*"])
    else:
        suggest_invoices = frappe.get_all("Sales Invoice", filters={"operator" : username.full_name}, fields=["*"])
        invoices = frappe.get_all("Sales Invoice", filters={"operator" : username.full_name}, fields=["*"])

    customers = set()
    for i in invoices:
        customers.add(i.customer)
    
    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.invoices = invoice_list
    context.suggest_invoices = suggest_invoices
    context.all_invoices = invoices
    context.params = form_d
    context.customer = customers
    context.user_type = customer_group
    if "page" not in form_d:
        context.next_page = 2
        context.prev_page = 0
    else:
        if int(form_d["page"]) == 0:
            context.next_page = int(form_d['page']) + 2
        else:
            context.next_page = int(form_d['page']) + 2

        if int(form_d["page"]) == 1:
            context.prev_page = 0
        else:
            context.prev_page = int(form_d["page"]) - 1
  