// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Mother Policy', {
// 	// refresh: function(frm) {

// 	// }
// });


frappe.ui.form.on('Mother Policy', {
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