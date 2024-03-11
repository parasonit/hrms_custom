import frappe

@frappe.whitelist()
def calculate_age(birthdate):
    birthdate = frappe.utils.getdate(birthdate)
    today_date = frappe.utils.getdate(frappe.utils.today())
    age = today_date.year - birthdate.year - ((today_date.month, today_date.day) < (birthdate.month, birthdate.day))
    return age

