// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on("Activity Master", {
    onload: function(frm){
        filterChildFields(frm, "levels_of_activity", "supplier_group", "policy_provider")
        function filterChildFields(frm, tableName, fieldName, fieldFiltered) {
            frm.fields_dict[tableName].grid.get_field(fieldFiltered).get_query = function(doc, cdt, cdn) {
                return {    
                    filters:[
                        [fieldName, '=', "Insurance Provider"]
                    ]
                }
            }
        }
    }
})