frappe.ui.form.on('Job Requisition', {
    validate(frm) {
        if (frm.doc.custom_position_type === 'Replacement' && frm.doc.no_of_positions > 1) {
            frappe.validated = false;
            frappe.throw({
                title: __('Validation Error'),
                message: __('The number of positions for a <b>Replacement</b> cannot exceed <b>1</b>.')
            });
        }


        if (frm.doc.custom_replacement_) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Job Requisition',
                    fields: ['name'],
                    filters: {
                        custom_replacement_: frm.doc.custom_replacement_,
                        workflow_state: ['not in', ['Rejected', 'Rejected by HR Manager', 'Rejected by HR Head', 'Rejected by Director']],
                        name: ["!=", frm.doc.name]
                    }
                },
                async: false,
                callback: function(response) {
                    if (response.message.length >0) {
                        frappe.validated = false; 

                        frappe.throw({
                            title: __('Validation Error'),
                            message: __('A job requisition with this Replacement already exists.')
                        });
                    }
                }
            });
        }

    },


    refresh(frm) {
             
        if (frm.is_new()) {
            frappe.db.get_value('Employee', { user_id: frappe.session.user }, 'name', ({ name }) => {
                frm.set_value('requested_by', name);
            });
        }
    },
    after_workflow_action(frm) {
        const status_map = {
            'Approved by HR Manager':'Open & Approved',
            'Approved by HR Head': 'Open & Approved',
            'Approved by Director': 'Open & Approved',
            'Rejected by HR Manager': 'Rejected',
            'Rejected by HR Head': 'Rejected',
            'Rejected by Director': 'Rejected',
            'Approved': 'Open & Approved',
            'Rejected': 'Rejected'
        };
        frm.set_value('status', status_map[frm.doc.workflow_state] || 'Pending');
        frm.save();

        if (frm.doc.workflow_state === 'Approved'){
            frappe.call({
                method: "hrms_custom.doc_events.make_job_opening",
                args: {
                    source_name: frm.doc.name,
                    designation:frm.doc.designation
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.show_alert(r.message);
                    }
                }
            });
        }
        
        
    }
});
