// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Annual Membership', {
	setup: function(frm) {
		frm.set_query("policy_provider", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Supplier', 'supplier_group', '=', "Insurance Provider"],
				]
			};
		});
	},
});
