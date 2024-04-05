// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Membership Issuance', {
	setup: function(frm) {
		frm.set_query("policy_provider", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Supplier', 'supplier_group', '=', "Insurance Provider"],
				]
			};
		});
		frm.set_query("plan", function(doc, cdt, cdn) {
			if (!frm.doc.membership_id){
				frappe.msgprint("Please enter Membership ID before selecting Plan.")
			}else{
				return {
					filters: [
						['Item', 'item_group', '=', "Annual Membership"],
						["Item","membership_id", "in", [frm.doc.membership_id]]
					]
				};
			}
		});
	},
});
