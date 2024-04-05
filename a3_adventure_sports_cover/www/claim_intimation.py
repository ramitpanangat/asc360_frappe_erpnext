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
    filters = {}


    if len(form_d)>0:
        #Filter with Booking Name
        if form_d["name"] != "":
            filters["name"] = form_d["name"]
        

    claims= frappe.get_all("Claim Intimation", fields=["*"], filters=filters)
 
    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.params = form_d
    context.claims = claims