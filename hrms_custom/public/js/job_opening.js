frappe.ui.form.on("Job Opening", {
	refresh(frm, cdt, cdn) {
        if(frm.doc.__islocal){
            frappe.db.get_value('Employee', {'user_id': frappe.session.user}, 'name')
            .then(r => {
                let employee = r.message;
                frm.set_value("custom_reporting_manager", employee.name)
            })

            //update Request Flow Staff
            frm.set_value("custom_request_flow_staff", frappe.session.user)
        }

        //filter Employees Replacement
        frm.set_query('custom_employees_replacement', function(doc, cdt, cdn) {
            return {
                "filters": [
                    ["Employee", "leave_approver", "=", frappe.session.user]
                ]
            };
        });
	}

})