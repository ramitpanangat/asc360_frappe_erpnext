
var cust_list = []
frappe.ui.form.on("B2B Policy Issue", {

	operator: function(frm){
		if (frm.doc.policy_issued_by == "Operator"){
		frappe.call({
			method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.get_customised_policy",
			args: {
				operator: frm.doc.operator,
			},
			callback: function(r){
				cust_list = r.message
				refresh_field("policy_name")
			}
		});
	}
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
	
	refresh: function(frm){
		if(frm.doc.docstatus==1){
			frm.page.clear_secondary_action()
			if(frm.doc.policy_type=="Single Policy"){
				frm.page.set_secondary_action("Cancel", () => {
					frappe.confirm("This will permanently cancel this policy.", ()=>{
						frappe.call({
							method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.cancel_document",
							args: {
								document:frm.doc.name,
								batch_id: frm.doc.batch_id
							},
							callback: function(r){
								cur_frm.refresh()
							} 
					})
					}, ()=>{})
				})
			}else{
				if(frm.doc.pdf_added == "In Process"){
					frm.add_custom_button("Add to Queue", ()=>{
						frappe.call({
							method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.add_to_queue",
							args: {batch:frm.doc.name},
							callback: (result)=>{
								frappe.msgprint(`${result.message}`)
							}
						})
					})
				}
			}
			// frm.add_custom_button("Cancel", function(){
				
			// }).removeClass('btn-default').addClass('btn-danger');
			downloadBtn(frm);
		}
		frm.set_query("policy_name", function() {
			return {
				filters: [
					["Customised Policy","docstatus", "in", ["1"]],
					["Customised Policy","status", "=", "Active"],
					["Customised Policy","operator_status", "=", "Approved"],
				]
			}
			// if (cust_list.length>0){
			// 	return {
			// 		filters: [
			// 			["Customised Policy","name", "in", cust_list],
			// 			["Customised Policy","docstatus", "in", ["1"]],
			// 			["Customised Policy","status", "=", "Active"],
			// 		]
			// 	}
			// }else{
			// 	frappe.msgprint("Please select an operator before selecting the policy.")
			// }
		});
	},
	setup: function(frm) {
		
		frm.set_query("policy", function() {
			var period_of_issuance = frappe.datetime.get_day_diff(frm.doc.end_date , frm.doc.start_date)
			if (!frm.doc.start_date || !frm.doc.end_date || !frm.doc.policy_name){
				frappe.msgprint("Please enter Journey Start Date, Journey End Date and Policy Name before selecting Plan.")
			}else{
				return {
					filters: [
						["Item","parent_policy", "in", [frm.doc.policy_name]],
						["Item","period_of_issuance", "in", [`${period_of_issuance+1}`]],
					]
				}
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
	
	frm.fields_dict["policy_list"].grid.add_custom_button('Download', 
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
	frm.fields_dict["policy_list"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-secondary');
	frm.fields_dict["policy_list"].grid.grid_buttons.find('.grid-add-row').addClass('hidden');
	$('*[data-fieldname="policy_list"]').find('.grid-remove-rows').hide()
	$('*[data-fieldname="policy_list"]').find('.grid-remove-all-rows').hide()
	$('*[data-fieldname="policy_cancelled"]').find('.grid-remove-rows').hide()
	$('*[data-fieldname="policy_cancelled"]').find('.grid-remove-all-rows').hide()
	frm.fields_dict["policy_cancelled"].grid.grid_buttons.find('.grid-add-row').addClass('hidden');
};
