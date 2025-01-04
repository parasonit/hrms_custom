// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Appointment Letter', {

	onload_post_render: function (frm) {
		addFieldEventListeners(frm);
		frm.doc.appointment_letter_template && updateTemplateFieldsVisibility(frm);
	},

	appointment_letter_template(frm) {
		if (frm.doc.appointment_letter_template) {
			updateTemplateFieldsVisibility(frm);
			updateAppointmentTemplate(frm);
		} else {
			hideAllFields(frm);
		}
	},

	before_save(frm) {
		frm.doc.appointment_letter_template && updateAppointmentTemplate(frm);
	}
});



const addFieldEventListeners = frm => {
	Object.keys(frm.fields_dict.custom__appointment_letter_terms.fields_dict).forEach(fieldName => {
		$(`[data-fieldname="${fieldName}"]`).on('change', () => {
			frm.doc.appointment_letter_template && updateAppointmentTemplate(frm);
		});
	});
};

const updateTemplateFieldsVisibility = frm => {
	frappe.db.get_value('Appointment Letter Template', frm.doc.appointment_letter_template, 'custom_template_format', ({ custom_template_format }) => {
		const requiredFields = new Set(custom_template_format.match(/\{\{(.*?)\}\}/g).map(match => match.replace(/\{\{|\}\}/g, '').trim()));
		const fields = frm.fields_dict.custom__appointment_letter_terms.fields_dict;
		Object.keys(fields).forEach(fieldName => {
			const isRequired = requiredFields.has(fieldName);
			frm.toggle_display(fieldName, isRequired);
			frm.toggle_reqd(fieldName, isRequired);
		});
	});
};

const updateAppointmentTemplate = frm => {
	frappe.call({
		method: "hrms_custom.doc_events.render_appointment_template",
		args: {
			appt_template: frm.doc.appointment_letter_template,
			doc: frm.doc
		},
		callback: response => {
			!response.exc && frm.set_value("custom_appointment_format", response.message);
		}
	});
};


const hideAllFields = frm => {
	Object.keys(frm.fields_dict.custom__appointment_letter_terms.fields_dict).forEach(fieldName => {
		frm.toggle_display(fieldName, false);
		frm.toggle_reqd(fieldName, false);
	});
};