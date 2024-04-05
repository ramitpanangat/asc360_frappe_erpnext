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
    filters = {"raised_by": username.email}

    if len(form_d)>0:
        #Filter with Booking Name
        if form_d["name"] != "":
            filters["name"] = form_d["name"]
        
        #Filter with Nature_of Activity
        if form_d["nature_of_activity"] != "":
            filters["nature_of_activity"] = form_d["nature_of_activity"]

        

    bookings = frappe.get_all("Issue", filters=filters, fields=["*"])
    all_bookings = frappe.get_all("Booking", filters={"operator": username.full_name}, fields=["*"])
    operator_booking = frappe.get_meta("Booking")

    nature_of_activity = operator_booking.get_field("nature_of_activity").options.split("\n")

    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = '/images/avatar.png'
    else:
        context.pro_pic = username.user_image

    context.bookings = bookings
    context.all_bookings = all_bookings
    context.nature_of_activities = nature_of_activity
    context.params = form_d