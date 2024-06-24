frappe.ui.form.on('Employee Referral', {
    refresh(frm) {

        if (frm.is_new()) {
            frappe.db.get_value('Employee', { user_id: frappe.session.user }, 'name', ({ name }) => {
                frm.set_value('referrer', name);
            });
        }

        frm.set_query("custom_current_designation", "hrms_custom.query_condition.designation_query");

        frm.set_query("for_designation", "hrms_custom.query_condition.designation_query");


    }

});
