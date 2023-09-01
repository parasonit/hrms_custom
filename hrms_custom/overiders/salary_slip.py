import frappe

@frappe.whitelist()
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


sql_query = """
    SELECT
    SUM(CASE WHEN status = 'On Leave' THEN 1 ELSE 0 END) as on_leave_count,
    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_count
    FROM `tabAttendance` 
    WHERE attendance_date BETWEEN %(from_date)s AND %(to_date)s 
    AND employee = %(employee)s
    AND company = %(company)s
"""

days = frappe.db.sql(
    sql_query,{"employee": doc.employee,"from_date": doc.start_date, "to_date": doc.end_date,"company":doc.company},as_dict=True)
    
actual_day = int(frappe.utils.date_diff(doc.end_date, doc.start_date)) +1

doc.actual_day = actual_day

doc.weekly_off = actual_day - doc.total_working_days
if days[0].get('on_leave_count'):
    doc.leave_with_pay = days[0].get('on_leave_count')
if days[0].get('present_count'):
    doc.present_days = days[0].get('present_count')



if doc.pay_group in ['Contractual','Worker']:
    total_attendance_request = calculate_total_attendance_request(doc)
    doc.arrear_days = total_attendance_request
    
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

    
if doc.pay_group == 'staff':
    total_attendance_request = calculate_total_attendance_request(doc)
    assumption_day = calculate_assumption_day(doc)
    doc.arrear_days = total_attendance_request - assumption_day + leave_arrear(doc)


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
    
doc.save()

# non_zero_deductions = []

# for row in doc.deductions:
#     if row.amount<=0:
#         print(str(row.idx))
#     else:
#         non_zero_deductions.append(row)

# doc.deductions = non_zero_deductions

# doc.save()
        