// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Staffing Plan', {
	setup: function(frm) {
		frm.set_query("designation", "staffing_details", function() {
			let designations = [];
			(frm.doc.staffing_details || []).forEach(function(staff_detail) {
				if(staff_detail.designation){
					designations.push(staff_detail.designation)
				}
			})
			// Filter out designations already selected in Staffing Plan Detail
			return {
				filters: [
					['Designation', 'name', 'not in', designations],
				]
			}
		});

		frm.set_query("department", function() {
			return {
				"filters": {
					"company": frm.doc.company,
				}
			};
		});
	},

	get_job_requisitions: function(frm) {
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Job Requisition",
			target: frm,
			date_field: "posting_date",
			add_filters_group: 1,
			setters: {
				designation: null,
				requested_by: null,
			},
			get_query() {
				let filters = {
					company: frm.doc.company,
					status: ["in", ["Pending", "Open & Approved"]],
				}

				if (frm.doc.department)
					filters.department = frm.doc.department;

				return {
					filters: filters
				};
			},
			action(selections) {
				const plan_name = frm.doc.__newname;
				frappe.call({
					method: "set_job_requisitions",
					doc: frm.doc,
					args: selections,
				}).then(() => {
					// hack to retain prompt name that gets lost on frappe.call
					frm.doc.__newname = plan_name;
					refresh_field("staffing_details");
				});

				cur_dialog.hide();
			}
		});
	},
	total_estimated_budget(frm){
        update_total_estimated_cost_of_department(frm);
	},
	custom_total_current_cost(frm){
        update_total_estimated_cost_of_department(frm);
	}
});

frappe.ui.form.on('Staffing Plan Detail', {
	designation: function(frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if(frm.doc.company && child.designation) {
			set_number_of_positions(frm, cdt, cdn);
			set_cost_of_current_count(frm,cdt,cdn)
		}
	},
	custom_department: function(frm, cdt, cdn){
		let child = locals[cdt][cdn];
		if(frm.doc.company && child.designation && child.custom_department) {
			set_number_of_positions(frm, cdt, cdn);
			set_cost_of_current_count(frm,cdt,cdn)
		}
	},
	vacancies: function(frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if(child.vacancies < child.current_openings) {
			frappe.throw(__("Vacancies cannot be lower than the current openings"));
		}
		set_number_of_positions(frm, cdt, cdn);
		set_total_count(frm, cdt, cdn)
		set_total_estimated_vacancies(frm,cdt,cdn)
	},

	current_count: function(frm, cdt, cdn) {
		set_number_of_positions(frm, cdt, cdn);
	},

	estimated_cost_per_position: function(frm, cdt, cdn) {
		set_total_estimated_cost(frm, cdt, cdn);
	}
});

var set_number_of_positions = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn];
	if (!child.designation) frappe.throw(__("Please enter the designation"));
	frappe.call({
		"method": "hrms.hr.doctype.staffing_plan.staffing_plan.get_designation_counts",  
		args: {
			designation: child.designation,
			company: frm.doc.company,
			department: child.custom_department
		},
		callback: function (data) {
			if(data.message){
				frappe.model.set_value(cdt, cdn, 'current_count', data.message.employee_count);
				frappe.model.set_value(cdt, cdn, 'current_openings', data.message.job_openings);
				let total_positions = cint(data.message.employee_count) + cint(child.vacancies);
				// if (cint(child.number_of_positions) < total_positions){
				// 	frappe.model.set_value(cdt, cdn, 'number_of_positions', total_positions);
				// }
				frappe.model.set_value(cdt, cdn, 'number_of_positions', total_positions);
			}
			else{ // No employees for this designation
				frappe.model.set_value(cdt, cdn, 'current_count', 0);
				frappe.model.set_value(cdt, cdn, 'current_openings', 0);
			}
		}
	});
	refresh_field("staffing_details");
	set_total_estimated_cost(frm, cdt, cdn);
	set_total_count(frm, cdt, cdn);

}

// Note: Estimated Cost is calculated on number of Vacancies
var set_total_estimated_cost = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn]
	if(child.vacancies > 0 && child.estimated_cost_per_position) {
		frappe.model.set_value(cdt, cdn, 'total_estimated_cost', child.vacancies * child.estimated_cost_per_position);
	}
	else {
		frappe.model.set_value(cdt, cdn, 'total_estimated_cost', 0);
	}
	set_total_estimated_budget(frm);
};

var set_total_estimated_budget = function(frm) {
	let estimated_budget = 0.0
	if(frm.doc.staffing_details) {
		(frm.doc.staffing_details || []).forEach(function(staff_detail) {
			if(staff_detail.total_estimated_cost){
				estimated_budget += staff_detail.total_estimated_cost
			}
		})
		frm.set_value('total_estimated_budget', estimated_budget);
	}
};

var set_cost_of_current_count = function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];

    frappe.call({
        method: "hrms_custom.doc_events.get_total_cost",
        args: {
            designation: child.designation,
            company: frm.doc.company,
            department: child.custom_department
        },
        callback: function (data) {
            let cost = data.message || 0;
            frappe.model.set_value(cdt, cdn, 'custom_cost_of_current_count', cost);
            refresh_field("staffing_details");
            set_total_current_cost(frm);
        }
    });
};


var set_total_count = function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    let total_count = (child.vacancies || 0) + (child.current_count || 0);
    frappe.model.set_value(cdt, cdn, 'custom_total_count', total_count);
    set_total_current_count(frm);
    refresh_field("staffing_details");
};

var set_total_current_cost = function (frm) {
    let total_current_cost = (frm.doc.staffing_details || []).reduce((total, detail) => {
        return total + (detail.custom_cost_of_current_count || 0);
    }, 0);
    frm.set_value('custom_total_current_cost', total_current_cost);
};


var set_total_estimated_vacancies = function (frm) {
    let estimated_vacancies = (frm.doc.staffing_details || []).reduce((total, detail) => {
        return total + (detail.vacancies || 0);
    }, 0);
    frm.set_value('custom_total_estimated_vacancies', estimated_vacancies);
    refresh_field("staffing_details");
};

var set_total_current_count = function (frm) {
    let total_current_count = (frm.doc.staffing_details || []).reduce((total, detail) => {
        return total + (detail.custom_total_count || 0);
    }, 0);
    frm.set_value('custom_total_current_count', total_current_count);
};

var update_total_estimated_cost_of_department = function(frm) {
    let total_estimated_cost_of_department = (frm.doc.total_estimated_budget || 0) + (frm.doc.custom_total_current_cost || 0);
    frm.set_value("custom_total_estimated_cost_of_department", total_estimated_cost_of_department);
};
