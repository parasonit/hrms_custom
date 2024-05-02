// Copyright (c) 2024, 8848 and contributors
// For license information, please see license.txt

frappe.query_reports["Appraisal Pending By Employee"] = {
	"filters": [
		{
			"fieldname": "appraisal_cycle",
			"fieldtype": "Link",
			"label": __("Appraisal Cycle"),
			"options": "Appraisal Cycle",
		}
	]
};
 