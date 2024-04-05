from frappe import get_doc, get_value, db


def validate(doc, event):
    if doc.customer_group == "Operator Customer":
        operator = get_value("Operator", doc.customer_name, "email")
        if db.exists("Contact", {"first_name":doc.customer_name, "email_id": operator}):
            contact = get_doc("Contact", {"first_name":doc.customer_name, "email_id": operator})
            doc.customer_primary_contact = contact.name