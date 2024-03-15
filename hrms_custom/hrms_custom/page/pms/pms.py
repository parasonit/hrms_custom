import frappe
from frappe import _
from urllib.parse import quote

hr_staff = ["System Manager", "HR Manager", "HR User"]
def get_context(context):
    cards = get_cards()
    context.data = cards


def active_employees(role=None):
    if role in hr_staff:
        total_active_employees = len(frappe.db.get_list('Employee',
            filters={
                'status': 'Active',
                "custom_pms_eligibility": ("!=", "Not Applicable")
            },
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":  
        total_active_employees = len(frappe.db.get_list('Employee',
            filters={
                'status': 'Active',
                'leave_approver': frappe.session.user,
                "custom_pms_eligibility": ("!=", "Not Applicable")
            },
            fields=['name'],
            as_list=True
        ))

    return total_active_employees or 0

def appr_pending_by_employees(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update filters
        # filters = {
        #     'workflow_state': 'Draft'
        # }
        # if appraisal_cycle:
        #     filters.update({
        #         "appraisal_cycle": appraisal_cycle
        #     })
        #     total_appraisal = len(frappe.db.get_list('Appraisal',
        #         filters=filters,
        #         fields=['name'],
        #         as_list=True
        #     ))

        # else:

        total_active_employee = active_employees(role="System Manager")
        appraisal_submited_by_emp = appr_submitted_by_emp(role="System Manager", appraisal_cycle=appraisal_cycle)
        total_appraisal = int(total_active_employee) - int(appraisal_submited_by_emp)

    elif role == "Leave Approver":
        #update filters
        # filters = {
        #     'workflow_state': 'Draft',
        #     'custom_approver': frappe.session.user
        # }

        # if appraisal_cycle:
        #     filters.update({
        #         "appraisal_cycle": appraisal_cycle
        #     })

        # total_appraisal = len(frappe.db.get_list('Appraisal',
        #     filters=filters,
        #     fields=['name'],
        #     as_list=True
        # ))
        
        total_active_employee = active_employees(role="Leave Approver")
        appraisal_submited_by_emp = appr_submitted_by_emp(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        total_appraisal = int(total_active_employee) - int(appraisal_submited_by_emp)

    return total_appraisal or 0

def appr_pending_by_rm(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update filters
        filters = {
            'workflow_state': 'Approval Pending By Reporting Manager'
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":
        #update filters
        filters = {
            'workflow_state': 'Approval Pending By Reporting Manager',
            'custom_approver': frappe.session.user
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    
    return total_appraisal or 0

def appr_pending_by_hr(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update filters
        filters = {
            'workflow_state': 'Approval Pending By HR Manager'
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":
        #update filters
        filters = {
                'workflow_state': 'Approval Pending By HR Manager',
                'custom_approver': frappe.session.user
            }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))

    return total_appraisal or 0
    
def appr_pending_by_dir(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update filters
        filters = {
                'workflow_state': 'Approval Pending By Director'
            }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":
        #update filters
        filters = {
            'workflow_state': 'Approval Pending By Director',
            'custom_approver': frappe.session.user
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))

    return total_appraisal or 0


def appr_completed(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update filters
        filters = {
            'workflow_state': 'Approved'
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":
        #update filters
        filters = {
            'workflow_state': 'Approved',
            'custom_approver': frappe.session.user
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })
        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    return total_appraisal or 0

def appr_submitted_by_emp(role=None, appraisal_cycle=None):
    if role in hr_staff:
        #update Filter
        filters = {
            "workflow_state": ["in", ["Approval Pending By Reporting Manager", "Approval Pending By HR Manager", "Approval Pending By Director", "Approved"]],
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    elif role == "Leave Approver":
        #update filters
        filters = {
            "workflow_state": ["in", ["Approval Pending By Reporting Manager", "Approval Pending By HR Manager", "Approval Pending By Director", "Approved"]],
            'custom_approver': frappe.session.user
        }
        if appraisal_cycle:
            filters.update({
                "appraisal_cycle": appraisal_cycle
            })

        total_appraisal = len(frappe.db.get_list('Appraisal',
            filters=filters,
            fields=['name'],
            as_list=True
        ))
    return total_appraisal or 0

@frappe.whitelist()
def get_cards(appraisal_cycle=None):
    cards = []
    #review submitted by employee
    base_url = f"{frappe.utils.get_url()}/app/appraisal"
    workflow_state = '["in",["Approval Pending By Reporting Manager","Approval Pending By HR Manager","Approval Pending By Director","Approved"]]'
    encoded_workflow_state = quote(workflow_state, safe='')
    url = f"{base_url}?workflow_state={encoded_workflow_state}&appraisal_cycle={appraisal_cycle}"

    roles = frappe.get_roles(frappe.session.user)


    if "System Manager" in roles or "HR Manager" in roles or "HR User" in roles:
        total_active_employee = active_employees(role="System Manager")
        appraisal_submited_by_emp = appr_submitted_by_emp(role="System Manager", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_employee = appr_pending_by_employees(role="System Manager", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_rm = appr_pending_by_rm(role="System Manager", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_hr = appr_pending_by_hr(role="System Manager", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_dir = appr_pending_by_dir(role="System Manager", appraisal_cycle=appraisal_cycle)
        appraisal_completed = appr_completed(role="System Manager", appraisal_cycle=appraisal_cycle)        

        cards = [
            {
                "name": "Eligible Employees",
                "total": total_active_employee,
                "route": "employee?status=Active"
            },
            {
                "name": "Review Submitted By Employee",
                "total": appraisal_submited_by_emp,
                "route": url
            },
            {
                "name": "Review Pending By Employee",
                "total": pending_appraisal_by_employee,
                "route": f"appraisal?workflow_state=Draft&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By Reporting Manager",
                "total": pending_appraisal_by_rm,
                "route": f"appraisal?workflow_state=Approval Pending By Reporting Manager&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By HR Manager",
                "total": pending_appraisal_by_hr,
                "route": f"appraisal?workflow_state=Approval Pending By HR Manager&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By Director",
                "total": pending_appraisal_by_dir,
                "route": f"appraisal?workflow_state=Approval Pending By Director&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Completed",
                "total": appraisal_completed,
                "route": f"appraisal?workflow_state=Approved&appraisal_cycle={appraisal_cycle}"
            }
        ]
        
    elif "Leave Approver" in roles:
        total_active_employee = active_employees(role="Leave Approver")
        appraisal_submited_by_emp = appr_submitted_by_emp(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_employee = appr_pending_by_employees(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_rm = appr_pending_by_rm(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_hr = appr_pending_by_hr(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        pending_appraisal_by_dir = appr_pending_by_dir(role="Leave Approver", appraisal_cycle=appraisal_cycle)
        appraisal_completed = appr_completed(role="Leave Approver", appraisal_cycle=appraisal_cycle)

        cards = [
            {
                "name": "Eligible Employees",
                "total": total_active_employee,
                "route": f"employee?status=Active&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Submitted By Employee",
                "total": appraisal_submited_by_emp,
                "route": url
            },
            {
                "name": "Review Pending By Employee",
                "total": pending_appraisal_by_employee,
                "route": f"appraisal?workflow_state=Draft&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By Reporting Manager",
                "total": pending_appraisal_by_rm,
                "route": f"appraisal?workflow_state=Approval Pending By Reporting Manager&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By HR Manager",
                "total": pending_appraisal_by_hr,
                "route": f"appraisal?workflow_state=Approval Pending By HR Manager&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Pending By Director",
                "total": pending_appraisal_by_dir,
                "route": f"appraisal?workflow_state=Approval Pending By Director&appraisal_cycle={appraisal_cycle}"
            },
            {
                "name": "Review Completed",
                "total": appraisal_completed,
                "route": f"appraisal?workflow_state=Approved&appraisal_cycle={appraisal_cycle}"
            }
        ]
            
    return cards


