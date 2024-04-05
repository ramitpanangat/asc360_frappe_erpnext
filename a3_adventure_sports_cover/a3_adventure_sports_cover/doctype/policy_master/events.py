import json
from frappe import get_doc
import frappe
from json import loads

@frappe.whitelist()
def get_table_datas(mother_policy):
	parent_policy = get_doc("Mother Policy", mother_policy)
	insurance_plan_details = parent_policy.insurance_plan_details
	policy_premium = parent_policy.policy_premium
	activity_list = parent_policy.activity_list
	return {"insurance_plan_details": insurance_plan_details, "policy_premium": policy_premium, "activity_list": activity_list}