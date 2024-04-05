import frappe

def validate(doc, events):
    if doc.attached_to_doctype == "Operator Bulk Policy":
        doc.is_private = 0