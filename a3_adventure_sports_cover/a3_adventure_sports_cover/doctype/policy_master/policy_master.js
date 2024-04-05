// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on("Policy Master", {
	setup: function(frm) {
		frm.set_query("parent_policy", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Mother Policy', 'docstatus', '=', 1],
					['Mother Policy', 'status', '=', "Active"],
				]
			};
		});
	},
	parent_policy: function(frm){
		if (frm.doc.package_policy == 0){
		frappe.call({
			method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.policy_master.events.get_table_datas",
			args: {
				mother_policy: frm.doc.parent_policy
			},
			callback: function(r){
				if (frm.doc.parent_policy){
					// Fetch Policy Insurance Plan details from Mother Policy
					frm.clear_table("insurance_plan_details")
					r.message.insurance_plan_details.forEach(element => {
						const insurance_plan_details = frm.add_child("insurance_plan_details")
						insurance_plan_details.policy_benefits = element.policy_benefits
						insurance_plan_details.plan_1 = element.plan_1
						insurance_plan_details.plan_2 = element.plan_2
						insurance_plan_details.plan_3 = element.plan_3
						insurance_plan_details.plan_4 = element.plan_4
						insurance_plan_details.plan_5 = element.plan_5
						insurance_plan_details.plan_6 = element.plan_6
						insurance_plan_details.plan_7 = element.plan_7
						insurance_plan_details.plan_8 = element.plan_8
						insurance_plan_details.plan_9 = element.plan_9
						insurance_plan_details.plan_10 = element.plan_10
						insurance_plan_details.deductible = element.deductible
						refresh_field("insurance_plan_details")
					});
					
					frm.clear_table("policy_premium")
					r.message.policy_premium.forEach(element => {
						const policy_premium = frm.add_child("policy_premium")
						policy_premium.maximum_trip_duration = element.maximum_trip_duration
						policy_premium.plan_1 = element.plan_1
						policy_premium.plan_2 = element.plan_2
						policy_premium.plan_3 = element.plan_3
						policy_premium.plan_4 = element.plan_4
						policy_premium.plan_5 = element.plan_5
						policy_premium.plan_6 = element.plan_6
						policy_premium.plan_7 = element.plan_7
						policy_premium.plan_8 = element.plan_8
						policy_premium.plan_9 = element.plan_9
						policy_premium.plan_10 = element.plan_10
						refresh_field("policy_premium")
					});
					
					frm.clear_table("activity_list")
					r.message.activity_list.forEach(element => {
						const activity_list = frm.add_child("activity_list")
						activity_list.activity_name = element.activity_name
						activity_list.level = element.level
						activity_list.mother_policy_level = element.mother_policy_level
						activity_list.category = element.category
						refresh_field("activity_list")
					});
				}
			}
		})
	}
	}
});
