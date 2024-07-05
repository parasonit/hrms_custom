frappe.ready(function() {
    // Set all fields to required
    Object.values(frappe.web_form.fields_dict).forEach(field => field.df.reqd = 1);

    // Set specific fields to read-only
    ['job_title', 'designation', 'applicant_name','department'].forEach(field => {
        frappe.web_form.fields_dict[field].df.read_only = 1;
    });

    frappe.web_form.refresh();

	frappe.web_form.after_save = () => {
		frappe.call({
            method: "hrms_custom.hrms_custom.web_form.job_application_form.job_application_form.update_job_application_status",
            args: {
                docname: frappe.web_form.doc.name
            }
        });

	}
});
