from calendar import month
from itertools import groupby
import frappe
from frappe import get_doc
import pandas as pd
from bs4 import BeautifulSoup

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] != "Website User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    username = get_doc("User", frappe.session.user)
    filters = {"operator": username.full_name}

    sales_summary = frappe.get_all("Sales Summary", filters=filters, fields=["*"])

    collection = []
    for item in sales_summary:
        sales_sum = frappe.get_doc("Sales Summary", item.name)
        for d in sales_sum.item_total:
            datas = {}
            datas["item"] = d.item
            datas[sales_sum.month] = d.total
            collection.append(datas)

    months = set()
    for k in collection:
        for key in k.keys():
            if key != 'item':
                months.add(key)

    df = pd.DataFrame(collection).groupby(['item']).max()
    
    replace_nan = df.fillna(0)
    replace_nan.loc[:,'Total'] = df.sum(numeric_only=True, axis=1)
    replace_nan.index.name = "Policy"
    replace_nan.round(2)
    items = replace_nan.to_html(classes=["table", "report_table"])

    context.table = items
    if username.user_image=="" or username.user_image==None:
        context.pro_pic = './assets/avatar.webp'
    else:
        context.pro_pic = username.user_image
