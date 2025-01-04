frappe.ui.form.on("Job Offer", {
    onload_post_render: function (frm) {
        addFieldEventListeners(frm);
        frm.doc.select_terms && updateTemplateFieldsVisibility(frm);
    },
    select_terms(frm) {
        if (frm.doc.select_terms) {
            updateTemplateFieldsVisibility(frm);
            handleDesignation(frm);
            updateJobOfferTemplate(frm);
        } else {
            hideAllFields(frm);
        }
    },
    validate: function (frm) {
        validatePincode(frm);
    }
})

const addFieldEventListeners = frm => {
    Object.keys(frm.fields_dict.custom_job_offer_terms.fields_dict).forEach(fieldName => {
        $(`[data-fieldname="${fieldName}"]`).on('change', () => {
            frm.doc.select_terms && updateJobOfferTemplate(frm);
        });
    });
};

const updateTemplateFieldsVisibility = frm => {
    frappe.db.get_value('Terms and Conditions', frm.doc.select_terms, 'terms', ({ terms }) => {
        const requiredFields = new Set(terms.match(/\{\{(.*?)\}\}/g).map(match => match.replace(/\{\{|\}\}/g, '').trim()));
        const conditionalFields = new Set(
            (terms.match(/\{% if .*? %\}\{\{(.*?)\}\}\{% endif %\}/g) || []).map(match => match.match(/\{\{(.*?)\}\}/)[1].trim())
        );
        Object.keys(frm.fields_dict.custom_job_offer_terms.fields_dict).forEach(fieldName => {
            const isRequired = requiredFields.has(fieldName);
            console.log(isRequired, fieldName)
            frm.toggle_display(fieldName, isRequired);
            if (!conditionalFields.has(fieldName)) {
                frm.toggle_reqd(fieldName, isRequired);
            }
            // if (!isRequired) {frm.set_value(fieldName, '');}
        });
    });
};

const hideAllFields = frm => {
    Object.keys(frm.fields_dict.custom_job_offer_terms.fields_dict).forEach(fieldName => {
        frm.toggle_display(fieldName, false);
        frm.toggle_reqd(fieldName, false);
    });
};

function handleDesignation(frm) {
    const { select_terms, designation } = frm.doc;
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
}

const updateJobOfferTemplate = frm => {
    erpnext.utils.get_terms(frm.doc.select_terms, frm.doc, function (r) {
        if (!r.exc) {
            frm.set_value("terms", r.message);
        }
    });
};

const validatePincode = frm => {
    if (frm.doc.custom_pincode && frm.doc.custom_pincode.toString().length !== 6) {
        frappe.msgprint({
            title: __('Validation Error'),
            message: __("Pincode must be a 6-digit number.")
        });
        frappe.validated = false;
    }
};