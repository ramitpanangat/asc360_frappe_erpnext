frappe.ready(function() {
	frappe.web_form.after_load = () => {

		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "User",
				name: frappe.session.user,
			},
			callback(r){
				if(r.message){
					frappe.call({
						method: "frappe.client.get",
						args: {
							doctype: "Operator",
							name: r.message.full_name,
						},
						callback(res){
							frappe.web_form.set_df_property("operator", "read_only", 0)
							frappe.web_form.set_value("operator", res.message.operator_name)
							frappe.web_form.set_df_property("operator", "read_only", 1)

							frappe.web_form.set_value("email", res.message.email)
							frappe.web_form.set_value("email_preference", res.message.email_preferences)
							frappe.call({
								method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.get_customised_policy",
								args: {
									operator: res.message.operator_name,
								},
								callback: function(r){
									var cus_list = []
									r.message.forEach((v)=>{
										cus_list.push({label:v.policy, value:v.policy})
									})
									var policy_name = frappe.web_form.get_field("policy_name")
									policy_name._data = cus_list
								}
							});
						}
					})
					frappe.web_form.on('policy_name', (field, value) => {
						if(value){
							frappe.call({
								method: "a3_adventure_sports_cover.a3_adventure_sports_cover.web_form.b2b_policy.b2b_policy.get_items",
								args: {customised_policy: value},
								callback: (items) => {
									var plans = [] 
									items.message.plans.forEach((item)=>{
										plans.push({label:item.name, value:item.name})
									})
									var plan_data = frappe.web_form.get_field('plan_name')
									plan_data._data = plans
								}
							})
						}
					})
					frappe.web_form.on('plan_name', (field, value)=>{
						if(value){
							frappe.call({
								method: "a3_adventure_sports_cover.a3_adventure_sports_cover.web_form.b2b_policy.b2b_policy.get_item_details",
								args: {item: value},
								callback: (detail) => {
									console.log(detail)
									frappe.web_form.set_value("premium_amount", detail.message.standard_rate)
									frappe.web_form.set_value("maximum_trip_duration", detail.message.period_of_issuance)
								}
							})

						}
					})
					frappe.call({
						method: "frappe.client.get",
						args: {
							doctype: "Operator Balance",
							name: r.message.full_name,
						},
						callback(ob) {
							if(ob.message) {
								frappe.web_form.set_value("operator_balance", ob.message.balance_available)
							}
						}
					});
				}
			}
		})

	}
})