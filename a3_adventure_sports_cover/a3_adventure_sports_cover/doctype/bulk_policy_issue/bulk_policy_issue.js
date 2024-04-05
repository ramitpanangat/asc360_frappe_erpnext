// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Policy Issue', {
	setup: function(frm) {
		frm.set_query("policy_provider", function() {
			return {
				filters: [
					["Supplier","supplier_group", "=", "Insurance Provider"],
				]
			}
		});
	}
});
