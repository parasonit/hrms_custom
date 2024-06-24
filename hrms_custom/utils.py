import frappe
from frappe.utils.password import get_decrypted_password
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, redirect_post_login
from datetime import datetime


import os
import shutil
import random
import string

from frappe import db, get_doc, get_site_path
current_year = datetime.now().year

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

def update_employee_documents():
    active_employees = frappe.get_list(
		"Employee",
		filters={'status': 'Active'},
		fields=["name"],
		pluck='name'
	)

    # update_emp_letter(employee="PMI-1383")

    for employee in active_employees:
        frappe.enqueue(
            update_emp_letter, employee = employee, queue="long", enqueue_after_commit=True
        )


def update_emp_letter(employee):
    if employee:
        doc = get_doc("Employee", employee)

        form_16_path = get_site_path('private', 'files', 'employee_letter', str(current_year), 'form-16')
        increment_letter_path = get_site_path('private', 'files', 'employee_letter', str(current_year), 'increment_letter')

        # Update form 16 files
        update_form_16(doc, form_16_path)

        # Update increment letter files
        update_increment_letter(doc, increment_letter_path)

def update_increment_letter(doc, increment_letter_path):
    increment_letter_files = os.listdir(increment_letter_path)

    for element in increment_letter_files:
        if element.startswith(doc.name):
            random_file = main(filename=element, original_directory=increment_letter_path, type="increment_letter")
            if random_file:
                doc.append("custom_increment_letter", {
                    'name1': random_file,
                    'year': current_year
                })
    doc.save()
    frappe.db.commit()
    
def update_form_16(doc, form_16_path):
    form_16_files = os.listdir(form_16_path)

    for element in form_16_files:
        random_file = main(filename=element, original_directory=form_16_path, type="form-16")
        
        if element.startswith(doc.pan_number+"_PARTB"):
            form_type = "PARTB"
        elif element.startswith(doc.pan_number):
            form_type = "FORM-16"
        
        if random_file:
            doc.append("custom_form_16", {
                'name1': random_file,
                'year': current_year,
                'type': form_type
            })

    doc.save()
    frappe.db.commit()
    
def generate_random_name(length=10):
    """Generate a random filename."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_unique_random_name(existing_names, length=10):
    """Generate a unique random filename."""
    while True:
        random_name = generate_random_name(length)
        if random_name not in existing_names:
            return random_name

def main(filename, original_directory, type):
    # Specify the directory containing the files

    # Specify the directory where the new files with random names will be created
    new_directory = get_site_path('private', 'files', 'random', type, str(current_year))

    # Ensure the new directory exists
    os.makedirs(new_directory, exist_ok=True)

    # Get existing names in the new directory to avoid duplicates
    existing_names = set(os.listdir(new_directory))

    if filename:
        # Generate a unique random filename
        random_filename = get_unique_random_name(existing_names) + os.path.splitext(filename)[1]
        existing_names.add(random_filename)  # Add the new name to the set

        # Construct the full paths
        original_path = os.path.join(original_directory, filename)
        new_path = os.path.join(new_directory, random_filename)

        # Copy the file to the new directory with the unique random name
        shutil.copy(original_path, new_path)

        # Remove the original file
        os.remove(original_path)
        
        return random_filename
