from hrms_custom.overiders.shift_type import custom_get_attendance
import frappe

def update_attendance(doc, method):
    if doc.docstatus == 1:
        query = f"""
            select name, employee, log_type, time, shift, shift_start, shift_end,
            shift_actual_start, shift_actual_end, device_id
            from `tabEmployee Checkin` 
            where name = "{doc.employee}" and time between "{doc.from_date}" and "{doc.to_date}"
        """
        checkin_logs = frappe.db.sql(query, as_dict=1)
        frappe.log_error("update_attendance", checkin_logs)
        shift_doc = frappe.get_doc("Shift Type", doc.shift_type)
        resp = custom_get_attendance(self=shift_doc, logs=checkin_logs)
        if resp:
            attendance = frappe.db.get_value('Attendance', {
                'employee': doc.employee, 
                'attendance_date': doc.from_date
            }, 'name')
            if attendance:
                frappe.db.set_value('Attendance', attendance, {
                    'status': resp[0],
                    'total_working_hours': resp[1],
                    'late_entry': resp[2],
                    'early_exit': resp[3],
                    'in_time': resp[4],
                    'out_time': resp[5]
                })
                frappe.db.commit()

def update_user_permission(doc, method):
    if frappe.db.exists("Employee", doc.name):
        leave_approver = frappe.db.get_value('Employee', doc.name, 'leave_approver')
        if leave_approver != doc.leave_approver:
            #remove old permission
            frappe.db.delete("User Permission", {
                "user": leave_approver,
                "allow": "Employee",
                "for_value": doc.name 
            })

            #insert User Permission
            insert_user_permission(doc)
    else:
        insert_user_permission(doc)

def insert_user_permission(doc):
    roles = frappe.get_roles(doc.leave_approver)
    if "HR Manager" in roles or "HR User" in roles:
        return
    else:
        doc = frappe.get_doc({
            'doctype': 'User Permission',
            "user": doc.leave_approver,
            "allow": "Employee",
            "for_value": doc.name,
            "apply_to_all_doctypes": 1
        })
        doc.insert()
        frappe.db.commit() 

# def update_kra_goal_score(doc, method):
#     if doc.workflow_state == "Saved":
#         for goal in doc.goals:
#             for self_kra in doc.custom_self_appraisal_kra:
#                 if self_kra.kra == goal.kra:
#                     self_kra.custom_self_score = self_kra.score
#                     goal.custom_self_score = self_kra.score
#                     break
        