// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Operator Commission Payable', {
	refresh: function(frm) {
		if (frm.doc.status=="Unpaid"){
			frm.page.set_indicator(frm.doc.status, "grey")
		}
		else if(frm.doc.status=="Paid"){
			frm.page.set_indicator(frm.doc.status, "green")
		}
		else if(frm.doc.status=="Cancelled"){
			frm.page.set_indicator(frm.doc.status, "red")
		}
	}
});
