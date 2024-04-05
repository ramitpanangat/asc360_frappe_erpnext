import frappe
from frappe import get_doc, get_value, _, db
from datetime import datetime

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    
    form_d = frappe.form_dict

    username = get_doc("User", frappe.session.user)
    customer = get_doc("Customer", {"customer_name":username.full_name, "email_id": frappe.session.user})
    operator = get_doc("Operator", {"operator_name": customer.customer_name, "email": frappe.session.user})
    filters = {}

    for key in form_d:
        if key != 'page':
            if form_d[key] != "":
                filters[key] = form_d[key]

    invoices = frappe.get_all("Sales Invoice", filters={"operator": operator.name}, fields=["*"])
    b2b = frappe.get_all("B2B Policy Issue", filters={"operator": operator.name}, fields=["*"])
    payments = set()
    for policy in b2b:
        if db.exists("Payment Entry", {"policy_number": policy.name}):
            pay = get_doc("Payment Entry", {"policy_number": policy.name})
            payments.add(pay)
    for invoice in invoices:
        if db.exists("Payment Entry", {"party": invoice.customer, "paid_amount": invoice.grand_total}):
            payment = get_doc("Payment Entry", {"party": invoice.customer, "paid_amount": invoice.grand_total})
            if "mode_of_payment" in filters or "posting_date" in filters:
                if "mode_of_payment" in filters:

                    if filters["mode_of_payment"] == payment.mode_of_payment:
                        if len(payments)>0:
                            hasData = False
                            for p in payments:
                                if p.name == payment.name:
                                    hasData = True
                            if not hasData:
                                payments.add(payment)
                        else:
                                payments.add(payment)

                if "posting_date" in filters:
                    filter_date = filters["posting_date"]
                    pay_date = payment.posting_date
                    if isinstance(filter_date, str):
                        filter_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
                    if isinstance(pay_date, str):
                        pay_date = datetime.strptime(pay_date, "%Y-%m-%d").date()
                    if filter_date == pay_date:
                        if len(payments)>0:
                            hasData = False
                            for p in payments:
                                if p.name == payment.name:
                                    hasData = True
                            if not hasData:
                                payments.add(payment)
                        else:
                                payments.add(payment)
            else:
                if len(payments)>0:
                    hasData = False
                    for p in payments:
                        if p.name == payment.name:
                            hasData = True
                    if not hasData:
                        payments.add(payment)
                else:
                        payments.add(payment)

    mops = frappe.db.get_list("Mode of Payment")
    mode_of_payment = []
    for mop in mops:
        mode_of_payment.append(mop.name)

    username = get_doc("User", frappe.session.user)

    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.mode_of_payment = mode_of_payment
    context.params = form_d
    context.payments = payments
    context.user_type = customer.customer_group
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