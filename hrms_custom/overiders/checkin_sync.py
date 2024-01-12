import pyodbc
import json
import datetime
from datetime import datetime as dt, timedelta
import time
import configparser
import frappe
import os


# @frappe.whitelist()
def record_transactions():
    frappe.log_error("record_transactions", "Schedular Working")

    last_sync_datetime = frappe.get_last_doc('Employee Checkin').time

    # SQL Server Connection
    connection_string = (
    r"DRIVER=ODBC Driver 18 for SQL Server;"
    r"SERVER=192.168.0.48,1433;"
    r"DATABASE=COSEC;"
    r"UID=zinhr_dbuser;"
    r"PWD=0E$2MS_Dia32@F#F0;"
    r"TrustServerCertificate=yes;"
    )
    sql_conn = pyodbc.connect(connection_string)
    mycursor = sql_conn.cursor()

    # Calculate the last sync datetime in string format for the SQL query
    last_sync_datetime_str = last_sync_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # SQL Query to fetch transactions since the last sync using parameterized query
    query = f"SELECT * FROM dbo.VIEW_HRONE WHERE Edatetime >= ? AND Edatetime <= ?"
    end_date = dt.now()

    mycursor.execute(query, (last_sync_datetime_str,end_date))

    # Iterate through the SQL Server query result and create 'Employee Checkin' documents
    for row in mycursor:
        try:
            # Prepare the data for the Employee Checkin document using SQL Server data
            employee_name = row.UsrRefCode
            checkin_datetime = row.Edatetime

            employee_checkin = frappe.new_doc("Employee Checkin")
            # employee_checkin.employee = employee_name
            employee_checkin.employee = frappe.db.get_value('Employee',{'attendance_device_id':employee_name},'name')
            print("origin",row,employee_name,employee_checkin.employee,checkin_datetime,row.Edatetime)
            employee_checkin.time = checkin_datetime.strftime('%Y-%m-%d %H:%M:%S')
            employee_checkin.insert(ignore_permissions=True)

        except Exception as e:
            print(f"Error creating Employee Checkin: {str(e)}")

    # Close the cursor and connection
    mycursor.close()
    sql_conn.close()
    frappe.log_error('biometric sync done',f" at {last_sync_datetime}")

