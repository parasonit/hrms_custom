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
