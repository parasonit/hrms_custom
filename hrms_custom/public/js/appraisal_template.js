frappe.ui.form.on("Appraisal Template", {
	custom_fiscal_year(frm, cdt, cdn){
		//update template Title
		let temp_title = frm.doc.custom_employee + "-FY-" + frm.doc.custom_fiscal_year
		frm.set_value("template_title", temp_title)
	},
	refresh(frm, cdt, cdn) {
		frm.set_query("custom_key_activity", "goals", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['kra', '=', d.key_result_area]
				]
            }
        })
		//update employee
		if(frm.doc.__islocal){
			frappe.db.get_value('Employee', {user_id: frappe.session.user}, 'name')
			.then(r => {
				frm.set_value("custom_employee", r.message.name)

				//update template Title
				let temp_title = frm.doc.custom_employee + "-FY-" + frm.doc.custom_fiscal_year
				frm.set_value("template_title", temp_title)
			})
		}
	}
})

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