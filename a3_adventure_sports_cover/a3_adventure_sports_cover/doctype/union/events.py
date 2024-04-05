from frappe import get_doc, msgprint, new_doc, sendmail
import frappe




def on_submit(doc, event):
	user = get_doc({
        "doctype": "User",
        "first_name": doc.union_name,
        "email": doc.email
    })
	user.insert()	
	msgprint("User created!")