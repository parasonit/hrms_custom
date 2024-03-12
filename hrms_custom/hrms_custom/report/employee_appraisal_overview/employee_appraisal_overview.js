// Copyright (c) 2024, 8848 and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Appraisal Overview"] = {
	filters: [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "appraisal_cycle",
			"fieldtype": "Link",
			"label": __("Appraisal Cycle"),
			"options": "Appraisal Cycle",
		},
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": __("Employee"),
			"options": "Employee",
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation"
		},
		{
			"fieldname": "custom_branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch"
		}
	]
};

setTimeout(() => {
	$(".dt-instance-1 .dt-cell__content--col-0").css({"width":"50px"});
}, 500);
