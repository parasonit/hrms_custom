import frappe

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
# searches for leads which are not converted


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def designation_query(doctype, txt, searchfield, start, page_len, filters):
    sql_query = f"""
        SELECT {searchfield}, description 
        FROM `tab{doctype}`
    """
    conditions = []
    if filters:
        conditions.extend([f"`{key}` = '{value}'" for key, value in filters.items()])

    if txt:
        txt_condition = f"({searchfield} LIKE '%{txt}%' OR description LIKE '%{txt}%')"
        conditions.append(txt_condition)

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)
    
    sql_query += " ORDER BY CASE WHEN name = 'Other' THEN 1 ELSE 0 END, name"

    return frappe.db.sql(sql_query)
