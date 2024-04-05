import frappe

@frappe.whitelist()
def get_table_data(parent_policy):
    policy_master = frappe.get_doc("Policy Master", parent_policy)
    policy_premium = policy_master.policy_premium
    insurance_plan_details = policy_master.insurance_plan_details
    activity_list = policy_master.activity_list
    return {
        "insurance_plan_details": insurance_plan_details,
        "policy_premium": policy_premium,
        "activity_list": activity_list
    }