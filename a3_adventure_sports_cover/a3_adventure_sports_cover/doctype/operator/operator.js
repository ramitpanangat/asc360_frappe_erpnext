// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Operator', {
	refresh: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Sales Invoice"), function() {
				frappe.new_doc('Sales Invoice', {
					"customer": cur_frm.doc.operator_name
				});
			});
		}

		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Payment Entry"), function() {
				frappe.new_doc('Payment Entry', {
					"party_type": "Customer"
				});
			});
		}
	}
});
