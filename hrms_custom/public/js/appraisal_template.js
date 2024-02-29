frappe.ui.form.on("Appraisal Template Goal", {
	key_result_area(frm, cdt, cdn) {
		let d = frappe.get_doc(cdt, cdn);
        frappe.db.get_value('KRA', {name: d.key_result_area}, ['description', 'custom_metric'])
        .then(r => {
            let values = r.message;
            d.custom_key_activities = values.description
            d.metric = values.custom_metric
        })
        frm.refresh_fields("goals")
	}
})