import frappe

from erpnext.setup.doctype.employee.employee import (
	InactiveEmployeeStatusError,
	get_holiday_list_for_employee,
)

@frappe.whitelist()
def salary_slip(doc,method):
    
    def get_holidays_for_employee(
        employee, start_date, end_date, raise_exception=True):
        """Get Holidays for a given employee

        `employee` (str)
        `start_date` (str or datetime)
        `end_date` (str or datetime)
        `raise_exception` (bool)
        `only_non_weekly` (bool)

        return: list of dicts with `holiday_date` and `description`
        """
        holiday_list = get_holiday_list_for_employee(employee, raise_exception=raise_exception)

        if not holiday_list:
            return []

        filters = {"parent": holiday_list, "holiday_date": ("between", [start_date, end_date])}

        holidays = frappe.get_all("Holiday", fields=["description", "holiday_date","weekly_off"], filters=filters, order_by="holiday_date")
        
        week_off = 0
        paid_holiday = 0
        for row in holidays:
            if row.weekly_off:
                week_off  += 1
            else:
                paid_holiday += 1

        return week_off,paid_holiday
    doc.weekly_off ,doc.paid_holidays=get_holidays_for_employee( doc.employee, doc.start_date, doc.end_date)

    def calculate_total_attendance_request(doc):
        arrear_query = """
            SELECT 
                SUM(CASE WHEN status != 'Half Day' THEN 1 ELSE 0 END) as other_type,
                SUM(CASE WHEN status = 'Half Day' THEN 1 ELSE 0 END) as half_day
            FROM `tabAttendance`
            WHERE attendance_request IS NOT NULL 
                AND attendance_date BETWEEN %(from_date)s AND %(to_date)s 
                AND employee = %(employee)s
                AND company = %(company)s
        """
        
        arrear_days = frappe.db.sql(arrear_query, {
            "employee": doc.employee,
            "from_date": frappe.utils.add_to_date(doc.start_date, months=-1),
            "to_date": frappe.utils.get_last_day(frappe.utils.add_to_date(doc.end_date, months=-1)),
            "company": doc.company
        }, as_dict=True)
        
        total_arrear_days = 0
        if arrear_days[0].get('other_type'):
            total_arrear_days = arrear_days[0].get('other_type')  
        if arrear_days[0].get('half_day'):
            total_arrear_days = arrear_days[0].get('half_day')*0.5
        
        return total_arrear_days
        
    def calculate_total_leave_application(doc):
        leave_application_query = """
            SELECT 
                SUM(CASE WHEN status = 'On Leave' AND docstatus = 1 THEN 1 ELSE 0 END) as leave_count,
                SUM(CASE WHEN status = 'On Leave' AND docstatus = 2 THEN 1 ELSE 0 END) as leave_cancel_count
            FROM `tabAttendance`
            WHERE leave_application IS NOT NULL
                AND modified BETWEEN %(from_date)s AND %(to_date)s 
                AND employee = %(employee)s
                AND company = %(company)s
        """
        
        from_date = frappe.utils.add_to_date(doc.start_date, months=-1)
        
        leave_application_days = frappe.db.sql(leave_application_query, {
            "employee": doc.employee,
            "from_date": from_date,
            "to_date": frappe.utils.get_last_day(frappe.utils.add_to_date(doc.end_date, months=-1)),
            "company": doc.company
        }, as_dict=True)
        
        # frappe.msgprint(f"leave application {leave_application_days}")
        
        total_leave_application_days = 0
        if leave_application_days[0].get('leave_count'):
            total_leave_application_days = leave_application_days[0].get('leave_count')  
        if leave_application_days[0].get('leave_cancel_count'):
            total_leave_application_days = leave_application_days[0].get('leave_cancel_count')
        return total_leave_application_days
        
    def calculate_assumption_day(doc):
        last_arrear_query = """
            SELECT 
                SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent
            FROM `tabAttendance`
            WHERE attendance_request IS NULL 
                AND attendance_date BETWEEN %(from_date)s AND %(to_date)s 
                AND employee = %(employee)s
                AND company = %(company)s
        """
        from_date = frappe.utils.add_to_date(doc.start_date, months=-1)
        from_date = frappe.utils.add_to_date(doc.start_date, days=-6)
        
        last_arrear_days = frappe.db.sql(last_arrear_query, {
            "employee": doc.employee,
            "from_date": from_date,
            "to_date": frappe.utils.get_last_day(frappe.utils.add_to_date(doc.end_date, months=-1)),
            "company": doc.company
        }, as_dict=True)
        
        if last_arrear_days:
            return last_arrear_days[0].absent
        else:
            return 0
            
    def leave_arrear(doc):
        leave_arrear_query = """
            SELECT 
                SUM(CASE WHEN status = 'On Leave' AND docstatus = 1 THEN 1 ELSE 0 END) as leave_count,
                SUM(CASE WHEN status = 'On Leave' AND docstatus = 2 THEN 1 ELSE 0 END) as leave_cancel_count
            FROM `tabAttendance`
            WHERE attendance_date BETWEEN %(first_date)s AND %(last_date)s 
                AND modified BETWEEN %(from_date)s AND %(to_date)s 
                AND employee = %(employee)s
                AND company = %(company)s
        """
        
        from_date = frappe.utils.add_to_date(doc.start_date, months=-1)
        from_date = frappe.utils.add_to_date(doc.start_date, days=-6)
        
        last_date = frappe.utils.add_to_date(doc.start_date, days=-7)
        leave_arrear_days = frappe.db.sql(leave_arrear_query, {
            "employee": doc.employee,
            "from_date": from_date,
            "to_date": frappe.utils.get_last_day(frappe.utils.add_to_date(doc.end_date, months=-1)),
            "first_date": doc.start_date,
            "last_date": last_date,
            "company": doc.company
        }, as_dict=True)
        
        total_leave_arrear_days = 0
        if leave_arrear_days[0].get('leave_count'):
            total_leave_arrear_days = leave_arrear_days[0].get('leave_count')  
        if leave_arrear_days[0].get('leave_cancel_count'):
            total_leave_arrear_days = leave_arrear_days[0].get('leave_cancel_count')

        return total_leave_arrear_days
        

    sql_query = """
        SELECT
        SUM(CASE WHEN status = 'On Leave' THEN 1 ELSE 0 END) as on_leave_count,
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_count,
        SUM(CASE WHEN overtime_hours > 0 THEN overtime_hours ELSE 0 END) as total_ot
        FROM `tabAttendance` 
        WHERE attendance_date BETWEEN %(from_date)s AND %(to_date)s 
        AND employee = %(employee)s
        AND company = %(company)s """

    days = frappe.db.sql(
        sql_query,{"employee": doc.employee,"from_date": doc.start_date, "to_date": doc.end_date,"company":doc.company},as_dict=True)
        
    actual_day = int(frappe.utils.date_diff(doc.end_date, doc.start_date)) +1

    doc.actual_day = actual_day

    # doc.weekly_off = actual_day - doc.total_working_days
    if days[0].get('on_leave_count'):
        doc.leave_with_pay = days[0].get('on_leave_count')
    if days[0].get('present_count'):
        doc.present_days = days[0].get('present_count')
    if days[0].get('total_ot'):
        doc.ot_hours = days[0].get('total_ot')

    if doc.pay_group in ['Contractual','Worker']:
        total_attendance_request = calculate_total_attendance_request(doc)
        doc.arrear_days = total_attendance_request + calculate_total_leave_application(doc)
        
        
    if doc.pay_group == 'Staff':
        total_attendance_request = calculate_total_attendance_request(doc)
        assumption_day = calculate_assumption_day(doc) or 0
        leave_arrear = leave_arrear(doc)
        # frappe.msgprint(f"{total_attendance_request}: {assumption_day}:{leave_arrear}")
        doc.arrear_days = total_attendance_request - assumption_day + leave_arrear


    previous_month_salary_querry = """
        SELECT 
            e.salary_component,e.amount,ss.payment_days
        FROM `tabSalary Slip` ss, `tabSalary Detail` e
        WHERE e.parent = ss.name
            AND start_date=%(from_date)s 
            AND end_date = %(to_date)s 
            AND employee = %(employee)s
            AND company = %(company)s
            # AND docstatus = 1
            # AND e.parentfield = 'earnings'
        """

    previous_month_salary = frappe.db.sql(previous_month_salary_querry, {
        "employee": doc.employee,
        "from_date": frappe.utils.add_to_date(doc.start_date, months=-1),
        "to_date": frappe.utils.get_last_day(frappe.utils.add_to_date(doc.end_date, months=-1)),
        "company": doc.company
        }, as_dict=True)


    if previous_month_salary:
        previous_salary_dict = {}
        payment_days = previous_month_salary[0].payment_days
        
        for item in previous_month_salary:
            previous_salary_dict[item['salary_component']] = item['amount']
        
        
        doc.basic1 = previous_salary_dict['Basic']
        doc.hra1 = previous_salary_dict['HRA']
        doc.conveyance1 = previous_salary_dict['Conveyance']
        doc.education_allowance1 = previous_salary_dict['Education Allowance']
        doc.personal_allowance1 = previous_salary_dict['Personal Allowance']
        doc.pf_amount1 = previous_salary_dict['Provident Fund']
        doc.last_payment_days = payment_days
        if doc.pay_group in ['Contractual','Worker']:
            doc.five_s_allowance1 = previous_salary_dict['5S Allowance']
            if doc.pay_group in ['Worker']:
                doc.washing_allowance1 = previous_salary_dict['Washing Allowance']
                
    def create_allocate_leave(doc,leave_type,leave_number):
        first_day_of_next_month = frappe.utils.get_first_day(frappe.utils.add_to_date(doc.end_date, months=1))
        leave_allocation = frappe.get_doc({
            'doctype': 'Leave Allocation',
            'employee': doc.employee,
            'leave_type': leave_type,
            'from_date': first_day_of_next_month,
            'to_date': frappe.utils.get_last_day(first_day_of_next_month),
            'new_leaves_allocated':leave_number
            })
            
        leave_allocation.insert(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_mandatory=True, # insert even if mandatory fields are not set 
        )

    if doc.leave_type_group == 'Corporate Staff':
        leave_number = 2
        if doc.absent_days > 0:
            leave_number = round((doc.payment_days*leave_number/doc.total_working_days),2)
        
        create_allocate_leave(doc,"Corporate Staff - PL",leave_number)
        
    elif doc.leave_type_group == 'Plant staff':
        leave_number = 2.5
        if doc.absent_days > 0:
            leave_number = round((doc.payment_days*leave_number/doc.total_working_days),2)
        create_allocate_leave(doc,"Plant Staff - PL",leave_number)

    doc.save()

        