# import frappe

# super_user_role = ["HR Manager", "LMS User"]

# def appraisal_template_query_condition(user):
# 	user = user or frappe.session.user
# 	roles = frappe.get_roles(frappe.session.user)
	
# 	if user == "Administrator" or any(item in roles for item in super_user_role):
# 		return ""
	
# 	employee = frappe.db.get_value('Employee', {'user_id': user}, ['name'])
# 	return f"""
# 	    (`tabAppraisal Template`.custom_employee = "{employee}" 
# 		    OR
# 		`tabAppraisal Template`.custom_employee in (select name from `tabEmployee` 
# 		    where reports_to = "{employee}"
# 		))
# 	"""

# def appraisal_query_condition(user):
# 	user = user or frappe.session.user
# 	roles = frappe.get_roles(frappe.session.user)
	
# 	if user == "Administrator" or any(item in roles for item in super_user_role):
# 		return ""
	
# 	employee = frappe.db.get_value('Employee', {'user_id': user}, ['name'])
# 	return f"""
# 	    (`tabAppraisal`.employee = "{employee}" 
# 		    OR
# 		`tabAppraisal`.employee in (select name from `tabEmployee`
# 		    where reports_to = "{employee}"
# 		))
# 	"""