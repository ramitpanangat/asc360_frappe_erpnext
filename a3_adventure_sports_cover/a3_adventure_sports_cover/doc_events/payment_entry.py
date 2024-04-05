import frappe

def before_insert(doc, method):
    party = doc.party_name
    if frappe.db.exists("Customer",party):
        customer = frappe.get_doc("Customer",party)
        if customer.customer_group == "Operator Customer":
            operator = frappe.get_doc("Operator", party)
            doc.operator_payment = "Operator Payment"
            if not doc.email:
                if operator.email:
                    doc.email = operator.email

    if doc.make_this_customer == 1:
        get_customer = frappe.db.exists("Customer", {"customer_name":doc.party_data, "email_id":doc.email})
        if get_customer == None:
            customer = frappe.new_doc("Customer")
            customer.customer_name = doc.party_data
            customer.customer_group = "Individual"
            customer.territory = "India"
            customer.date_of_birth = doc.date_of_birth
            customer.email_id = doc.email
            customer.mobile_no = doc.phone_number
            customer.insert()
            doc.party = doc.party_data
            doc.party_name = doc.party_data
        else:
            doc.party = doc.party_data
            doc.party_name = doc.party_data


def on_submit(doc, method):
    # if doc.party_type == "Customer":
    party = doc.party_name
    if frappe.db.exists("Customer",party):
        customer = frappe.get_doc("Customer",party)
        if customer.customer_group == "Operator Customer":
            if not frappe.db.exists("Operator Balance", party):
                pay = frappe.new_doc("Operator Balance")
                pay.operator = party
                pay.invoice_amount = float(doc.paid_amount)
                pay.balance_available = float(doc.paid_amount)
                pay.insert()
                frappe.msgprint("Operator Balance Created")
            else:
                pay = frappe.get_doc("Operator Balance", party)
                invoice_amount = float(pay.invoice_amount) + float(doc.paid_amount)
                balance_available = float(pay.balance_available) + float(doc.paid_amount)
                pay.invoice_amount = invoice_amount
                pay.balance_available = balance_available
                pay.save()