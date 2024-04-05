import frappe
from frappe import get_doc, _

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    form_d = frappe.form_dict
    username = get_doc("User", frappe.session.user)

    if frappe.request.environ["REQUEST_METHOD"] == "POST":
        if form_d["n_password"] == form_d["c_password"]:
            username.new_password = form_d["n_password"]
            username.save()
            form_d["message"] = "Password changed successfully."
            form_d["alert_color"] = "alert-success"
        else:
            form_d["message"] = "Please make sure password match."
            form_d["alert_color"] = "alert-danger"
    else:
        form_d = {}
        form_d["message"] = None


    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.params = form_d