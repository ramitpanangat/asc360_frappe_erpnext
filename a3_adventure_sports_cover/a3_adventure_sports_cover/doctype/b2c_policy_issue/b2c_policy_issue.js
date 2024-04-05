// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on("B2C Policy Issue", {
	refresh: function(frm){
		downloadBtn(frm)
	},
	customer_name: function(frm){
		frm.doc.customer = frm.doc.customer_name;
		refresh_field("customer")
		frappe.call({
			method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2c_policy_issue.events.get_customer_data",
			args :{customer: frm.doc.customer_name},
			callback: (res)=>{
				if (res.message != "No address found"){
					frm.set_value("address_line_1", res.message.address_line1)
					frm.refresh_field("address_line_1")
					frm.set_value("address_line_2", res.message.address_line2)
					frm.refresh_field("address_line_2")
					frm.set_value("citytown", res.message.city)
					frm.refresh_field("citytown")
					frm.set_value("state_ut", res.message.state)
					frm.refresh_field("state_ut")
					frm.set_value("country", res.message.country)
					frm.refresh_field("country")
					frm.set_value("pin_code", res.message.pincode)
					frm.refresh_field("pin_code")
				}
				console.log(res)
			}
		})
	},
	has_membership: function(frm){
		if (frm.doc.has_membership == "Yes"){
			frm.set_query("membership_id", function(){
				return {
					filters: [
						["Membership Issuance", "customer", "=", frm.doc.customer]
					]
				}
					
				})
		}
	},
	setup: function(frm) {
		frm.set_query("policy", function() {
			var period_of_issuance = frappe.datetime.get_day_diff(frm.doc.end_date , frm.doc.start_date)
			return {
				filters: [
					["Item","parent_policy", "in", [frm.doc.policy_name]],
					["Item","period_of_issuance", "in", [`${period_of_issuance+1}`]],
				]
			}
		});
		frm.set_query("policy_name", function() {
			return {
				filters: [
					["Customised Policy","docstatus", "in", ["1"]],
					["Customised Policy","status", "=", "Active"],
					["Customised Policy","operator_status", "=", "Approved"],
				]
			}
		});
		frm.set_query("policy_provider", function() {
			return {
				filters: [
					["Supplier","supplier_group", "=", "Insurance Provider"],
				]
			}
		});
	}
});


function downloadBtn(frm){
	
	frm.fields_dict["policy_generated_list"].grid.add_custom_button('Download', 
			function() {
				let checkedItem = frm.get_selected();
				var items = {"doc": frm.doc.name}
				var count = 0
				var c = 0
				checkedItem.policy_list.map(item => {
					items[count] = item
					count += 1
				})
				frappe.call({
					args: items,
					method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.bulk_download",
					callback: async function(r){
						console.log(r)
						for(var index=0; index <= Object.keys(r.message).length; index++){
							var link = document.createElement('a');
							link.href = r.message[index];
							link.download = r.message[index].substr(r.message[index].lastIndexOf('/') + 1);
							link.click();
							await new Promise(r => setTimeout(r, 1000));
						}
					}
				})
			});
	frm.fields_dict["policy_generated_list"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-secondary');
	frm.fields_dict["policy_generated_list"].grid.grid_buttons.find('.grid-add-row').addClass('hidden');
	$('*[data-fieldname="policy_generated_list"]').find('.grid-remove-rows').hide()
	$('*[data-fieldname="policy_generated_list"]').find('.grid-remove-all-rows').hide()
};
