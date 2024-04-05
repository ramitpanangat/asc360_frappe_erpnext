import frappe

def daily():
    policies = frappe.get_all("Policy Master")
    for policy in policies:
        doc = frappe.get_doc(policies["name"])
        if doc.policy_end_date < frappe.utils.nowdate():
            doc.status = "Inactive"
            doc.save()