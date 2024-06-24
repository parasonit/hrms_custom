
__version__ = '0.0.1'


from hrms.hr.doctype.employee_performance_feedback.employee_performance_feedback import EmployeePerformanceFeedback
from hrms_custom.overiders.employee_performance_feedback import custom_validate_total_weightage

EmployeePerformanceFeedback.validate_total_weightage = custom_validate_total_weightage


from hrms.hr.doctype.job_requisition.job_requisition import JobRequisition 
from hrms_custom.overrides import validate_duplicates

JobRequisition.validate_duplicates = validate_duplicates


from frappe.utils import response as _response
from hrms_custom.overrides import download_private_file
_response.download_private_file = download_private_file