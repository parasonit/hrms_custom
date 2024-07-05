import frappe

def get_context(context):
	# do your magic here
	pass


@frappe.whitelist()
def update_job_application_status(docname):
	frappe.db.sql("""
            UPDATE `tabJob Application`
            SET workflow_state = 'Details Updated by Applicant'
            WHERE name = %s
        """, (docname,))
	frappe.db.set_value("User", frappe.session.user, "enabled", 0)
	frappe.local.login_manager.logout()
	frappe.db.commit()
