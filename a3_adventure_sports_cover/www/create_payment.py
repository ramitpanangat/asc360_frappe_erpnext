from erpnext.erpnext_integrations.connectors.shopify_connection import get_url
import frappe
from frappe import get_doc, get_list, new_doc, _

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    
    form_d = frappe.form_dict
    mode_of_payment = get_list("Mode of Payment", fields=["*"])
    accounts = get_list("Account", fields=["*"])
    username = get_doc("User", frappe.session.user)

    if len(form_d)>0:
        pay = frappe.new_doc("Payment Entry")
        pay.party_type = "Customer"
        pay.party = username.full_name
        pay.party_name = username.full_name
        pay.paid_amount = form_d["amount_paid"]
        pay.received_amount = form_d["amount_paid"]
        pay.target_exchange_rate = 0.0
        pay.mode_of_payment = form_d["mode_of_payment"]
        pay.paid_to = form_d["account"]
        if form_d["reference_no"]:
            pay.reference_no = form_d["reference_no"]
        if form_d["reference_date"]:
            pay.reference_date = form_d["reference_date"]
        # pay.append("references", {
        #     "reference_doctype": "Sales Invoice",
        #     "reference_name" : invoice.name,
        #     "total_amount": self.premium_in_inr,
        #     "due_date": invoice.due_date,
        # })
        # self.payment_id = pay.name
        # self.db_update()
        pay.insert()


    context.username = username.full_name
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    context.mode_of_payment = mode_of_payment
    context.accounts = accounts