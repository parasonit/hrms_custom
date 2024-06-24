import frappe
from frappe.utils.nestedset import get_descendants_of

from frappe.utils.response import send_private_file
from werkzeug.wrappers import Response
from werkzeug.exceptions import Forbidden
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe import _
import os

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


def download_private_file(path: str) -> Response:
	"""Checks permissions and sends back private file"""
	files = frappe.get_all("File", filters={"file_url": path}, fields="*")
	# this file might be attached to multiple documents
	# if the file is accessible from any one of those documents
	# then it should be downloadable
	for file_data in files:
		file: "File" = frappe.get_doc(doctype="File", **file_data)
		if file.is_downloadable():
			break

	else:
		user_doc = frappe.get_doc("User", frappe.session.user)
		if user_doc.user_type == "System User":
			return send_private_file(path.split("/private", 1)[1])
		
		# raise Forbidden(_("You don't have permission to access this file"))
		
	
	make_access_log(doctype="File", document=file.name, file_type=os.path.splitext(path)[-1][1:])
	return send_private_file(path.split("/private", 1)[1])