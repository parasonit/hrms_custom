from . import __version__ as app_version

app_name = "hrms_custom"
app_title = "Hrms Custom"
app_publisher = "8848"
app_description = "Hrms customisation"
app_email = "jay@8848digital.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hrms_custom/css/hrms_custom.css"
# app_include_js = "/assets/hrms_custom/js/hrms_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/hrms_custom/css/hrms_custom.css"
# web_include_js = "/assets/hrms_custom/js/hrms_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hrms_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Appraisal" : "public/js/appraisal.js",
    "Appraisal Template": "public/js/appraisal_template.js",
    "Job Opening": "public/js/job_opening.js",
    "Employee": "public/js/employee.js"
}
doctype_list_js = {"Job Applicant" : "public/js/job_applicant_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "hrms_custom.utils.jinja_methods",
#	"filters": "hrms_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "hrms_custom.install.before_install"
# after_install = "hrms_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hrms_custom.uninstall.before_uninstall"
# after_uninstall = "hrms_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "hrms_custom.utils.before_app_install"
# after_app_install = "hrms_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "hrms_custom.utils.before_app_uninstall"
# after_app_uninstall = "hrms_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hrms_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

from hrms.hr.doctype.shift_type.shift_type import ShiftType
from hrms_custom.overiders.shift_attendance import process_auto_attendance
ShiftType.process_auto_attendance = process_auto_attendance


#override shift get_attendance
from hrms_custom.overiders.shift_type import custom_get_attendance
ShiftType.get_attendance = custom_get_attendance

# from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
# from hrms_custom.overiders.payroll_filters import get_emp_list
# PayrollEntry.get_emp_list = get_emp_list

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Payroll Entry": "hrms_custom.overiders.payroll_entry.PayrollEntry",
    "Appraisal": "hrms_custom.overiders.appraisal.CustomAppraisal"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Salary Slip": {
		"after_insert": "hrms_custom.overiders.salary_slip.salary_slip",
	},
    "Shift Request": {
        "on_submit": "hrms_custom.doc_events.update_attendance"
	},
    "Employee": {
        "validate": [
            # "hrms_custom.doc_events.update_user_permission",
            "hrms_custom.doc_events.validate_adhaar",
            "hrms_custom.doc_events.validate_pan",
            "hrms_custom.doc_events.validate_uan",
            "hrms_custom.doc_events.validate_pf",
            # "hrms_custom.doc_events.calculate_age"
        ]
	},
    "Job Opening": {
        "validate": [
            "hrms_custom.doc_events.update_job_opening_date",
            "hrms_custom.doc_events.validate_job_no"
		]
	},
    "Appraisal Template": {
        # "validate": {
        #     "hrms_custom.doc_events.auto_name_appr_temp"
		# },
        "before_insert": [
            "hrms_custom.doc_events.update_employee",
            "hrms_custom.doc_events.update_reporting_manager"
		]
	},
    "Job Offer": {
        "validate": "hrms_custom.doc_events.update_job_applicant_status",
        "on_trash": "hrms_custom.doc_events.update_job_applicant_status"
	},
    "Communication": {
        "validate": "hrms_custom.doc_events.update_job_applicant_status"
	},
    "Appraisal": {
        # "validate": "hrms_custom.doc_events.update_kra_goal_score"
        "autoname": "hrms_custom.doc_events.update_appraisal_name"
	}
}

# Scheduled Tasks
# ---------------


scheduler_events = {
    # "cron": {
	# 	"1 * * * *": [
	# 		"hrms_custom.overiders.checkin_sync.record_transactions",
	# 	],
	# },
	# "all": [
	# 	"hrms_custom.tasks.all"
	# ],
	"daily": [
		"hrms_custom.doc_events.calculate_age_daily"
	],
	"hourly_long": [
		"hrms_custom.overiders.checkin_sync.record_transactions"
	],
	# "weekly": [
	# 	"hrms_custom.tasks.weekly"
	# ],
	# "monthly": [
	# 	"hrms_custom.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "hrms_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "hrms_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "hrms_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["hrms_custom.utils.before_request"]
# after_request = ["hrms_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["hrms_custom.utils.before_job"]
# after_job = ["hrms_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"hrms_custom.auth.validate"
# ]

fixtures = [
    {"dt":"Custom Field","filters":[
        [
            "dt","in",[
                "Employee","Salary Structure","Salary Structure Assignment","Salary Slip",
                "Income Tax Slab","Appraisal Template","Appraisal","Appraisal Template-custom_department",
                "Shift Type","Holiday List", "Attendance Request-custom_approver", "Attendance Request-custom_approver_name",
                "Appraisal-custom_self_appraisal_kra", "Appraisal-custom_approver","Appraisal Template Goal-custom_key_activity",
            	"Appraisal-custom_is_final","Appraisal Goal-custom_key_activity","Appraisal Template-custom_designation",
                "Appraisal-final_score-description", "Appraisal-custom_approver_name", "Appraisal-custom_total_self_score",
                "Employee-custom_pms_eligibility", "Appraisal-custom_pms_eligibility", "Appraisal-custom_activities", 
                "Appraisal-custom_total_activity_score", "Appraisal-custom_total_activity_self_score","Appraisal-custom_score_conversion",
                "Appraisal-workflow_state","Appraisal Goal-custom_kras", "Job Opening-workflow_state","Job Opening-custom_employees_replacement",
                "Job Opening-custom_no_of_position","Job Opening-custom_required_experience","Job Opening-custom_qualification",
                "Job Opening-custom_grade","Job Opening-custom_reporting_manager","Job Opening-custom_salary","Job Opening-custom_minimum_salary",
                "Job Opening-custom_column_break_rguxs","Job Opening-custom_maximum_salary","Job Opening-custom_open_on","Employee-custom_account_details",
                "Employee-custom_column_break_tmpjf","Employee-custom_column_break_c8pfk","Employee-custom_sub_department",
                "Employee-custom_column_break_ydtct","Employee-custom_column_break_q4cfo","Employee-custom_column_break_68t5f",
                "Employee-custom_aadhaar_name","Employee-employment_type","Appraisal-custom_branch","Appraisal-main-field_order",
                "Appraisal Template-workflow_state","Appraisal Template-custom_reporting_manager","Leave Policy Assignment-custom_leave_type_group",
                "Job Offer-workflow_state","Appraisal Template-custom_employee","Employee-custom_company_mobile","Job Offer-custom_column_break_jk1xm",
                "Job Offer-custom_reporting_manager","Job Offer-custom_working_location","Job Offer-custom_sim_card","Job Offer-custom_column_break_ntjgz",
                "Job Offer-custom_mail_id","Job Offer-custom_mobile","Job Offer-custom_laptopdesktop","Job Offer-custom_assets_requirement","Job Offer-custom_interviewed_by",
                "Job Offer-custom_ctc","Job Offer-custom_ctc","Job Offer-custom_other_details","Appraisal Template-custom_department",
                "Appraisal Template-custom_column_break_x9jg9","Appraisal Template-custom_employee_name",
                "Appraisal Template Goal-custom_bsc","Appraisal Template Goal-custom_target","Appraisal Template Goal-custom_achieved_percentage",
                "Appraisal Template Goal-custom_metric","Appraisal Template Goal-custom_achieved","KRA-custom_metric"
            ]	
        ]
	]
},
{"dt":"Property Setter","filters":[
	[
		"doc_type","in",[
			"Employee","Salary Structure","Salary Structure Assignment","Salary Slip",
			"Income Tax Slab","Appraisal Template","Appraisal","Shift Type", "Holiday List", 
			"Appraisal-self_ratings-hidden", "Appraisal-section_break_23-label", "Appraisal-feedback_tab-hidden",
			"Appraisal-total_score-description", "Appraisal Goal-score_earned-hidden", "Appraisal Goal-score-label",
			"Appraisal Goal-kra-reqd", "Appraisal Goal-main-field_order", "Appraisal Goal-kra-columns", "Appraisal-self_appraisal_tab-depends_on",
			"Appraisal-self_score-hidden", "Appraisal-self_appraisal_tab-label", "Appraisal-feedback_tab-label",
			"Appraisal-feedback_tab-depends_on", "KRA-description-label","Appraisal Goal-kra-hidden","Appraisal Goal-kra-fetch_from",
			"Appraisal Goal-kra-in_list_view","Appraisal Goal-main-field_order", "Job Opening-closes_on-hidden","Job Opening-status-hidden",
            "Job Opening-closed_on-hidden","Job Opening-route-unique","Job Opening-status-in_standard_filter","Job Opening-job_title-in_list_view",
            "Job Opening-description-in_list_view","Job Opening-designation-in_list_view","Job Opening-custom_open_on-in_list_view",
            "Job Opening-custom_open_on-in_list_view","Job Opening-status-in_list_view","Job Opening-custom_no_of_position-in_list_view",
            "Employee-micr_code-hidden","Employee-iban-hidden","Employee-main-field_order","Employee-column_break_heye-hidden",
            "Employee-provident_fund_account-label","Job Applicant-status-options","Job Offer-workflow_state","Appraisal Template-rating_criteria-hidden",
            "Appraisal Template Goal-key_result_area-columns","Appraisal Template Goal-per_weightage-width","Appraisal Template Goal-per_weightage-columns",
            "Leave Policy Assignment-main-field_order","Employee-cell_number-label"
		]
	]
]},
{"dt": "Leave Type", "filters": [
	[
		"name", "in", [
			"Privilege Leave","Corporate Staff - PL","Plant Staff - PL","Compensatory Off",
			"Worker - CL","Worker - PL","SL - Apprentice Employee","CL - Apprentice Employee",
			"CL - Trainee Employee","ESIC",
		]
	]
]},
{"dt": "Shift Type", "filters": [
	[
		"name", "in", [
			"CMS","NS","FSS","FFS","TS","SS","FS","CG","FG",
		]
	]
]},
{"dt": "Income Tax Slab", "filters": [
	[
		"name", "in", [
			"New Regime Individual","Old Regime Super Senior Citizen","Old Regime Individual","Old Regime Senior Citizen",
		]
	]
]},
{"dt": "Salary Component", "filters": [
	[
		"name", "in", [
			"Arrear Basic","Arrear PF","Arrear Stipend","Arrear HRA","Arrear Conveyance","Arrear Personal Allowance",
			"Arrear 5S Allowance","Arrear Education Allowance","Arrear Washing Allowance","Arrear ESIC","Employer ESIC",
			"ESIC","Employer Pension","5S Allowance","Attendance Allowance","LWF","PF Basic","Employer LWF","PF Contribution",
			"Professional Tax","Personal Allowance","HRA","Annual Variable Pay","Bonus","Variable Pay","Other Earnings",
			"Incentive","Production Allowance","Overtime","HRA Static","Basic Static","Education Allowance Static",
			"Washing Allowance Static","Personal Allowance Static","Gate Pass Hrs","Gate Pass","Employer PF","Gross",
			"Gratuity","Conveyance Static Value","5S Allowance Static Value","Basic","Head","Leave Encashment","Provident Fund"
			,"Conveyance","Education Allowance","Washing Allowance","Stipend","Deputation Allowance","Notice Pay","Additional Tax",
			"Other Deduction","GSLI","LIC","Notice Recovery","Personal Loan","Salary Advance","Other",
		]
	]
]},
]