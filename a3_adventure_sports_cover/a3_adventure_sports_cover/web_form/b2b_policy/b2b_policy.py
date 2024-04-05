from __future__ import unicode_literals

import frappe

def get_context(context):
	pass

@frappe.whitelist()
def get_items(customised_policy):
	policy_provider = frappe.get_value("Customised Policy", customised_policy, "policy_provider")
	items = frappe.get_all("Item", filters={"parent_policy": customised_policy})
	return {"plans":items, "policy_provider": policy_provider}

@frappe.whitelist()
def get_item_details(item):
	item_detail = frappe.get_doc("Item", item).as_dict()
	return item_detail
