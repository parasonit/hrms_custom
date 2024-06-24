frappe.ui.form.on("Job Offer", {
    onload_post_render(frm) {
        Object.keys(frm.fields_dict.custom_job_offer_terms.fields_dict).forEach(fieldName => {
            $('[data-fieldname="' + fieldName + '"]').on('change', function () {
                erpnext.utils.get_terms(frm.doc.select_terms, frm.doc, function (r) {
                    if (!r.exc) {
                        frm.set_value("terms", r.message);
                    }
                });
            });
        });
    },
    refresh(frm) {


        loadTerms(frm);
    },

    select_terms(frm) {
        //can change order for better loading and opimizarin. need to check?
        resetFields(frm);
        loadTerms(frm);
        handleDesignation(frm);

    },
    //need to check and remove this if not needed
    before_save(frm) {
        erpnext.utils.get_terms(frm.doc.select_terms, frm.doc, function (r) {
            if (!r.exc) {
                frm.set_value("terms", r.message);
            }
        });
    },
    validate: function (frm) {
        if (frm.doc.custom_pincode) {
            if (frm.doc.custom_pincode.toString().length != 5) {
                frappe.msgprint({
                    title: __('Validation Error'),
                    message: __("Pincode must be a 5-digit number.")
                });
                frappe.validated = false;
            }
        }
    }
});

function resetFields(frm) {
    const fieldsDict = frm.fields_dict.custom_job_offer_terms.fields_dict;
    Object.keys(fieldsDict).forEach(fieldName => {
        frm.set_df_property(fieldName, 'hidden', 1);
        frm.set_df_property(fieldName, 'reqd', 0);
    });
}

function loadTerms(frm) {
    const { select_terms } = frm.doc;
    if (!select_terms) return;


    frappe.db.get_value('Terms and Conditions', select_terms, 'terms', ({ terms }) => {
        const { normalFields, conditionalFields } = extractFieldNames(terms);

        frm.set_df_property('custom_job_offer_terms', 'hidden', 0);

        normalFields.forEach(fieldName => {
            frm.set_df_property(fieldName, 'hidden', 0);
            frm.set_df_property(fieldName, 'reqd', 1);
        });

        conditionalFields.forEach(fieldName => {
            frm.set_df_property(fieldName, 'hidden', 0);
        });
    });
}

function extractFieldNames(htmlString) {
    const normalRegex = /\{\{(.*?)\}\}/g;
    const conditionalRegex = /\{%\s*if\s*(.*?)\s*%\}.*?\{\{\s*(.*?)\s*\}\}/gs;

    const normalFields = [];
    const conditionalFields = [];

    let match;
    while ((match = normalRegex.exec(htmlString)) !== null) {
        normalFields.push(match[1].trim());
    }

    let conditionalMatch;
    while ((conditionalMatch = conditionalRegex.exec(htmlString)) !== null) {
        const field = conditionalMatch[2].trim();
        const index = normalFields.indexOf(field);
        if (index !== -1) normalFields.splice(index, 1);
        conditionalFields.push(field);
    }

    return { normalFields, conditionalFields };
} 




function handleDesignation(frm) {
    const { select_terms, designation } = frm.doc;

    if (!select_terms) return;

    switch (select_terms) {
        case 'Offer Letter for Internship':
            frm.set_value("designation", 'Intern');
            frm.set_df_property('designation', 'read_only', 1);
            break;
        case 'Offer Letter for Training':
            frm.set_value("designation", 'Trainee');
            frm.set_df_property('designation', 'read_only', 1);
            break;
        case 'Offer Letter for Regular':
            if (designation === 'Intern' || designation === 'Trainee') {
                frm.set_value("designation", '');
                frm.set_df_property('designation', 'read_only', 0);
            }
            break;
        default:
            break;
    }

    erpnext.utils.get_terms(select_terms, frm.doc, function (r) {
        if (!r.exc) {
            frm.set_value("terms", r.message);
        }
    });
}
