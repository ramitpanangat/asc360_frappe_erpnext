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
    filters = {"payment_type": "Receive", "party": username.full_name }

    #TODO 1. check for frappe method to add multiple filters

    if len(form_d)>0:
        # Filter with Payment Type
        if form_d["payment_type"] != "":
            filters["payment_type"] = form_d["payment_type"]
        
        # Filter with Mode of Payment
        if form_d["mode_of_payment"] != "":
            filters["mode_of_payment"] = form_d["mode_of_payment"]
        
        # Filter with Posting Date
        if form_d["posting_date"] != "":
            filters["posting_date"] = form_d["posting_date"]
    
    
    payments = frappe.get_all("Payment Entry", filters=filters, fields=["*"])

    mops = frappe.db.get_list("Mode of Payment")
    mode_of_payment = []
    for mop in mops:
        mode_of_payment.append(mop.name)


    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.payments = payments
    context.mode_of_payment = mode_of_payment
    context.params = form_d
    context.user_type = customer_group