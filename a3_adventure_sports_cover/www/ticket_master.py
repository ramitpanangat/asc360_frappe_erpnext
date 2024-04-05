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
    filters = {"operator": username.full_name}

    if len(form_d)>0:
        #Filter with Product Name
        if form_d["name"] != "":
            filters["name"] = form_d["name"]

        #Filter with Package Type
        if form_d["package_type"] != "":
            filters["package_type"] = form_d["package_type"]

        #Filter with Package Category
        if form_d["package_category"] != "":
            filters["package_category"] = form_d["package_category"]
    
    products = frappe.get_all("Operator Product", filters=filters, fields=["*"])
    all_products = frappe.get_all("Operator Product", filters={"operator": username.full_name}, fields=["*"])
    operator_equipment = frappe.get_meta("Operator Product")

    package_categories = operator_equipment.get_field("package_category").options.split("\n")
    package_type = operator_equipment.get_field("package_type").options.split("\n")
    
    context.username = username.full_name

    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image

    context.products = products
    context.all_products = all_products
    context.package_types = package_type
    context.package_categories = package_categories
    context.params = form_d