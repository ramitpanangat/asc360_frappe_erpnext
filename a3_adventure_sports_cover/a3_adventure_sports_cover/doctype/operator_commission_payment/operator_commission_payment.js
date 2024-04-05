// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operator Commission Payment",{
	setup: function(frm){
		frm.set_query("paid_from", function(){
			return {
				filters: [["Account", "account_type", "in", ["Bank", "Cash"]],
						["Account", "is_group", "=", 0],
						["Account", "company", "=", "ASC360 Adventure Insurance"]]
			}
		})
	}
})