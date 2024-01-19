import frappe

def is_holiday(employee=None, date=None):
    """Returns true if the given date is a holiday in the given holiday list"""
    if employee and date:
        holiday_list = frappe.db.get_value('Employee', employee, 'holiday_list')
        if holiday_list:
            return bool(
                frappe.db.exists("Holiday", {"parent": holiday_list, "holiday_date": date})
            )
        else:
            return False