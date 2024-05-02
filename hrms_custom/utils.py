import frappe
from frappe.utils.password import get_decrypted_password
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, redirect_post_login

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

@frappe.whitelist(allow_guest=True)
def auth_url():
    client_secret = get_decrypted_password("Social Login Key", "office_365", "client_secret")
    if not client_secret:
        return
    auth_url = get_oauth2_authorize_url("office_365", "/app/performance")

    if frappe.local.conf.auto_login:
        return auth_url
    
    return