frappe.listview_settings['Sales Invoice'] = {
	onload: function(listview) {
		if (!frappe.route_options){ //remove this condition if not required
			frappe.route_options = {
				"b2c": ["=", "No"]
			};
		}
	}
};