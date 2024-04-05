// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('HAMRC Registration', {
	policy_no: function(frm) {
		if(frm.doc.policy_no){
			var policy = frappe.db.get_doc("List of Policy", frm.doc.policy_no).then(v => {
				var policy_doc = frappe.db.get_doc("List of Policy", v.policy).then(e=>{
					frm.set_value("participant_name", v.customer)
					frm.set_value("nationality", v.nationality)
					frm.set_value("gender", v.gender)
					frm.set_value("date_of_birth", v.date_of_birth)
					frm.set_value("contact_no", v.phone_number)
					frm.set_value("email_address", v.email_id)
				})
				
			})
			frm.refresh_field("participant_name")
			frm.refresh_field("nationality")
			frm.refresh_field("gender")
			frm.refresh_field("contact_no")
			frm.refresh_field("email_address")
			frm.refresh_field("date_of_birth")
		}
	}
});
