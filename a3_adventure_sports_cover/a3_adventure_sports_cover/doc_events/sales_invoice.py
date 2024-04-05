import frappe
import datetime

def on_submit(doc, method):
    if doc.posting_date:
        date =  datetime.datetime.strptime(doc.posting_date, "%Y-%m-%d")
        month_name = date.strftime("%b")
        doc.month = month_name
#############################################################################################

    # if doc.b2c == 0:
    #     if doc.grand_total:
    #         if frappe.db.exists("Sales Summary",{"operator": doc.operator, "month": doc.month}):
    #             summary = frappe.get_doc("Sales Summary",{"operator": doc.operator})
    #             if not summary.month:
    #                 summary.month = doc.month
    #             for row in doc.items:
    #                 summary.append("invoices",{
    #                 "policy": row.item_code,
    #                 "date": doc.posting_date,
    #                 "total": doc.grand_total
    #                 },
    #                 )
    #             if doc.operator:
    #                 summary.operator = doc.operator 
    #             summary.save()
    #         else:
    #             summary = frappe.new_doc("Sales Summary")
    #             if doc.operator:
    #                 summary.operator = doc.operator 
    #             if not summary.month:
    #                 summary.month = doc.month 
    #             for row in doc.items:
    #                 summary.append(
    #                     "invoices",
    #                         {
    #                     "policy": row.item_code,
    #                     "date": doc.posting_date,
    #                     "total": doc.grand_total
    #                     },
    #                 )
    #             summary.insert()

    # if doc.customer:
    #      for row in doc.items:
    #             if row.item_name == "Advance":
    #                 if frappe.db.exists("Customer",doc.customer):
    #                     customer = frappe.get_doc("Customer",doc.customer)
    #                     if customer.customer_group == "Operator Customer":
    #                         if frappe.db.exists("Operator Balance",doc.customer):
    #                             bal = frappe.get_doc("Operator Balance",doc.customer)
    #                             amount = bal.invoice_amount
    #                             total = bal.total_policy_amount
    #                             amount += doc.grand_total
    #                             new_bal = amount - total 
    #                             bal.invoice_amount = amount
    #                             bal.balance_available = new_bal 
    #                             bal.save()

    #                             frappe.msgprint("Operator Balance Updated!!")
    #                         else:
    #                             bal = frappe.new_doc("Operator Balance")
    #                             bal.operator = doc.customer
    #                             bal.invoice_amount = doc.grand_total
    #                             bal.balance_available = doc.grand_total
    #                             bal.insert()

    #                             frappe.msgprint("Operator Balance Record Created!!")