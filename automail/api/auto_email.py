
import frappe
from frappe import _
from frappe.desk.query_report import build_xlsx_data
from frappe.model.document import Document
from frappe.model.naming import append_number_if_name_exists
from frappe.utils import (
	add_to_date,
	cint,
	format_time,
	get_link_to_form,
	get_url_to_report,
	global_date_format,
	now,
	now_datetime,
	today,
	validate_email_address,
)
from frappe.utils.background_jobs import enqueue

import calendar
from datetime import timedelta

# Custom Code Start Here Dat 24Jul2023 For Send Email Specific Time Period
# schedule the email to be sent at the specified time
# @frappe.whitelist()


	
def get_time(*args):
	current_day = calendar.day_name[now_datetime().weekday()]
	enabled_reports = frappe.get_all(
		"Auto Email Report", filters={"enabled": 1, "frequency": ("in", ("Daily", "Weekdays", "Weekly"))}
	)
	for report in enabled_reports:
		auto_email_report = frappe.get_doc("Auto Email Report", report.name)
		if auto_email_report.frequency == "Weekdays":
			if current_day in ("Saturday", "Sunday"):
				continue
		elif auto_email_report.frequency == "Weekly":
			if auto_email_report.day_of_week != current_day:
				continue
		time = auto_email_report.cron_time
		# print (time)
		minute = time #"0"
		hour = "*"
		day_of_month = "*"
		month = "*"
		day_of_week = "*"
		time = f"{minute} {hour} {day_of_month} {month} {day_of_week}"
		# final = []
		# final.append(time[0][1])
		# print(final)
		return time
	
def schedule_email():
	current_day = calendar.day_name[now_datetime().weekday()]
	enabled_reports = frappe.get_all(
		"Auto Email Report", filters={"enabled": 1, "frequency": ("in", ("Daily", "Weekdays", "Weekly"))}
	)
	for report in enabled_reports:
		auto_email_report = frappe.get_doc("Auto Email Report", report.name)
		# if not correct weekday, skip
		if auto_email_report.frequency == "Weekdays":
			if current_day in ("Saturday", "Sunday"):
				continue
		elif auto_email_report.frequency == "Weekly":
			if auto_email_report.day_of_week != current_day:
				continue
		try:
			enqueue(auto_email_report.send(), queue='short', job_name='send_email', now=False, enqueue_after_commit=True)
		except Exception as e:
			auto_email_report.log_error(f"Failed to send {auto_email_report.name} Auto Email Report")