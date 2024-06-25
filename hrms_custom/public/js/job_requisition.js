frappe.ui.form.on('Job Requisition', {
    validate(frm) {

        frm.doc.custom_employment_type != 'Contractual' && validateDescriptionFields(frm);

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
                callback: function (response) {
                    if (response.message.length > 0) {
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

    frm.set_value("description",'description')     // Set default value for the description field to avoid mandatory error.

        customizeFileUploaderDialog(frm); // Customize file uploader dialog
        customizeDialogUploadOptions();


        if (frm.is_new()) {
            frappe.db.get_value('Employee', { user_id: frappe.session.user }, 'name', ({ name }) => {
                frm.set_value('requested_by', name);
            });
        }
    },
    after_workflow_action(frm) {
        const status_map = {
            'Approved by HR Manager': 'Open & Approved',
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

        if (frm.doc.workflow_state === 'Approved') {
            frappe.call({
                method: "hrms_custom.doc_events.make_job_opening",
                args: {
                    source_name: frm.doc.name,
                    designation: frm.doc.designation
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.show_alert(r.message);
                    }
                }
            });
        }
    }
});




// Function to customize file uploader dialog options
function customizeFileUploaderDialog(frm) {
    if (frm.doctype === 'Job Requisition') {
        frappe.ui.FileUploader.prototype.make_dialog = function (title) {
            this.dialog = new frappe.ui.Dialog({
                title: title || __("Upload"),
                primary_action_label: __("Upload"),

                // core code commented
                // primary_action: () => this.upload_files(),

                // custom code
                primary_action: validateAndUpload.bind(this),
                // custom code end

                secondary_action_label: __("Set all private"),
                secondary_action: () => {
                    this.uploader.toggle_all_private();
                },
                on_page_show: () => {
                    this.uploader.wrapper_ready = true;
                },
            });

            this.wrapper = this.dialog.body;
            this.dialog.show();
            this.dialog.$wrapper.on("hidden.bs.modal", function () {
                $(this).data("bs.modal", null);
                $(this).remove();
            });
        };
    }
}

// Function to validate file extension and handle upload
function validateAndUpload() {
    let fileExtension = this.dialog.body.innerText.split('\n')[0].trim().split('.').pop().toLowerCase();

    if (!['pdf', 'doc', 'docx'].includes(fileExtension)) {
        this.dialog.$wrapper.find('.file-action-buttons button:eq(1)').click();
        frappe.msgprint(__("Please attach a PDF, DOC, or DOCX file only."), __("Invalid File Type"), 'red');
    } else {
        this.upload_files();
    }
}


// Function to customize document upload options (removes Library and Link buttons)
function customizeDialogUploadOptions() {
    $('[data-fieldname="custom_document_upload"]').on('click', () => {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(function (mutation) {
                mutation.addedNodes.forEach(node => {
                    if ($(node).hasClass('modal')) {
                        $(node).find('button:contains("Library"), button:contains("Link")').remove();
                        $(node).find('input[type="file"]').attr('accept', '.pdf, .docx, .doc');
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

        setTimeout(() => observer.disconnect(), 500);
    });
}

function validateDescriptionFields(frm) {
    const validationErrors = [
        'custom_key_roles_and_responsibilities',
        'custom_knowledge_requirement',
        'custom_skill_requirement',
        'custom_behavioral_requirement'
    ]
    .map(field => {
        const fieldValue = frm.doc[field];
        if (fieldValue && fieldValue.trim().length < 100) {
            return `<b>${frm.get_field(field)._label}</b> must be at least 100 characters`;
        }
        return null; 
    })
    .filter(error => error !== null); 

    if (validationErrors.length > 0) {
        frappe.validated = false;
        frappe.throw({
            title: __('Validation Error'),
            message: validationErrors.join('<br>')
        });
    }
}
