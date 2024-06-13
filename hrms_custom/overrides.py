import frappe
from frappe.utils.nestedset import get_descendants_of

@frappe.whitelist()
def custom_get_designation_counts(designation, company, job_opening=None, department=None):
	frappe.log_error("get_designation_counts", department)
	if not designation:
		return False

	company_set = get_descendants_of("Company", company)
	company_set.append(company)

	filter = {"designation": designation, "status": "Active", "company": ("in", company_set)}

	if department:
		filter.update({'department': department})

	employee_count = frappe.db.count(
		"Employee", filter
	)

	filters = {"designation": designation, "status": "Open", "company": ("in", company_set)}

	if job_opening:
		filters["name"] = ("!=", job_opening)

	job_openings = frappe.db.count("Job Opening", filters)

	return {"employee_count": employee_count, "job_openings": job_openings}




def validate_duplicates(self):
    pass