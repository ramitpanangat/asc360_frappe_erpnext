// Copyright (c) 2022, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Issue Policy', {
    // policy : function (frm) {
    //
    //     if (frm.doc.policy) {
    //        frm.clear_table('plan_details');
    //         frappe.model.with_doc('Item', frm.doc.policy , function () {
    //             let source_doc = frappe.model.get_doc('Item', frm.doc.policy);
    //             $.each(source_doc.benefit_details, function (index, source_row) {
    //                const target_row = frm.add_child('plan_details');
    //                 target_row.benefits = source_row.benefit;
    //                 target_row.sum_insured = source_row.amount;
    //                 target_row.deductible = source_row.deductible;
    //                 frm.refresh_field('plan_details');
    //             });
    //         });
    //     }
    // }
});
