import frappe
from frappe import get_doc, get_value, _

no_cache = 1

def get_context(context):
    username = get_doc("User", frappe.session.user)
    customer_group = get_value("Customer", username.full_name, "customer_group")

    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    if customer_group == "Agent Customer":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict

    if frappe.request.environ["REQUEST_METHOD"] == "POST":
        if len(form_d)>0:
            if not frappe.db.exists("Issue", {"subject":form_d["subject"], "description": form_d["description"], "raised_by": username.email, "status": "Open"}):
                ticket = frappe.new_doc("Issue")
                ticket.subject = form_d["subject"]
                ticket.description = form_d["description"]
                ticket.save()
                form_d["message"] = "Ticket issued successfully."
                form_d["alert_color"] = "alert-success"
            else:
                form_d["message"] = "You have already submitted your ticket."
                form_d["alert_color"] = "alert-danger"
    else:
        form_d = {}
        form_d["message"] = None

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image
    context.username = username.full_name