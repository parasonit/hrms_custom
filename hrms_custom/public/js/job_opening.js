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

        //Prevent job Applicant creation when No of position full fill
        const hide_job_opening_btn = $('button.btn.btn-new.btn-secondary.btn-xs.icon-btn[data-doctype="Job Applicant"]')
        frappe.db.get_list('Job Applicant', {
            fields: ['name', 'job_title'],
            filters: {
                job_title: frm.doc.name,
                status: "Accepted"
            }
        }).then(records => {
            if(frm.doc.custom_position_type == "New" && records.length >= frm.doc.custom_no_of_position){
                hide_job_opening_btn.hide()
            }
            else if(frm.doc.custom_position_type == "Replacement" && records.length >= 1){
                hide_job_opening_btn.hide();
            }
        })
	}
})