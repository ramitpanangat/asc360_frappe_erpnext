// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('List of Policy', {
	refresh: function(frm) {
		if(frm.doc.policy_status=="Active"){
			frm.page.set_indicator("Active", "green")
		}else{
			frm.page.set_indicator("Cancelled", "grey")
		}

	}
});
