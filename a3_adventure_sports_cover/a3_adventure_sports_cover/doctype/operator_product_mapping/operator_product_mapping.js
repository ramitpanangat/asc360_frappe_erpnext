// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operator Product Mapping", {
    onload: function(frm){
        filterChildFields(frm, "customised_policy", "docstatus", "status", "policy")
        function filterChildFields(frm, tableName, fieldName, fieldName2, fieldFiltered) {
            frm.fields_dict[tableName].grid.get_field(fieldFiltered).get_query = function(doc, cdt, cdn) {
                return {    
                    filters:[
                        [fieldName, '=', 1],
                        [fieldName2, '=', "Active"],
                    ]
                }
            }
        }
    }
})
