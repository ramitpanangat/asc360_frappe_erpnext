// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Message Rule', {
	template: function(frm) {
		if (frm.doc.template_message){
			frappe.call({
				method:"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.whatsapp_message_rule.events.document_meta",
				args: {
					document: frm.doc.document_type,
					message: frm.doc.template_message
				},
				callback: (response)=>{
					var labelList = [];
					response.message.fields.forEach(element => {
						labelList.push(`${element.label} (${element.fieldname})`)
					});
					console.log(response.message)
					frappe.meta.get_docfield('WhatsApp Template Parameters', 'value', cur_frm.doc.name).options = labelList;
					cur_frm.refresh_field('parameter_mapping');

					frm.clear_table("parameter_mapping")
					response.message.parameters.forEach(element => {
						const parameters = frm.add_child("parameter_mapping")
						parameters.parameter = element
						refresh_field("parameter_mapping")
					});
				}
			})
		}

	}
});
