// Copyright (c) 2024, 8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Application", {
    async before_workflow_action(frm) {
        if (frm.doc.workflow_state == "Draft") {

            await frm.call("send_application_link").then(response => {
                if (response.message.status === "success") {
                    frappe.msgprint(response.message.message);
                } else if (response.message.status === "error") {
                    frappe.dom.unfreeze();
                    frappe.throw(response.message.message);
                }
            })
        }
        else if (frm.doc.workflow_state === 'Details Updated by Applicant') {
            await frm.call('convert_to_job_applicant').then(response => {
                if (response.message.status === "success") {
                    frappe.msgprint('The job application has been successfully converted to a job applicant.');
                } else if (response.message.status === "error") {
                    frappe.dom.unfreeze();
                    frappe.throw(response.message.message);
                }
            })
        }
    }
});
