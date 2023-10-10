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
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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

# from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
# from hrms_custom.overiders.payroll_filters import get_emp_list
# PayrollEntry.get_emp_list = get_emp_list

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Payroll Entry": "hrms_custom.overiders.payroll_entry.PayrollEntry"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Salary Slip": {
		"after_insert": "hrms_custom.overiders.salary_slip.salary_slip",
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
	# "daily": [
	# 	"hrms_custom.tasks.daily"
	# ],
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
                "Income Tax Slab","Appraisal Template","Appraisal",
                "Shift Type","Holiday List"
            ]
        ]
    ]
},
{"dt":"Property Setter","filters":[
        [
            "doc_type","in",[
                "Employee","Salary Structure","Salary Structure Assignment","Salary Slip",
                "Income Tax Slab","Appraisal Template","Appraisal",
                "Shift Type","Holiday List"
            ]
        ]
    ]
},
{"dt": "Holiday List", "filters": [
			[
				"name", "in", [
					"2023-Sat-Sun","2023-Saturday","2023-Friday","2023-Thursday","2023-Wednesday",
                    "2023-Tuesday","2023-Monday","2023-Sunday","2023",
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
        {"dt": "Salary Structure", "filters": [
			[
				"name", "in", [
					"Staff Test 1","Worker Test 3","Contractual Final",
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