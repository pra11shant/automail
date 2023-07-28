import frappe
from frappe.utils import *
import calendar
from datetime import timedelta
from frappe import _
from frappe.desk.query_report import build_xlsx_data
from frappe.model.document import Document
from frappe.model.naming import append_number_if_name_exists
@frappe.whitelist()
def send_hourly():
    frappe.log_error("log error in cron","TEST1")
    enabled_reports = frappe.get_all('Auto Email Report',
                                     filters={'enabled': 1})
    for report in enabled_reports:
        auto_email_report = frappe.get_doc('Auto Email Report', report.name)
        current_time = now_datetime().time()
        current = current_time.strftime("%H")
        print(current)
        print(auto_email_report.cron_time)
        try:
            if auto_email_report.cron_time == current:
                    frappe.log_error(current, "current time")
                    auto_email_report.send()
        except Exception as e:
                frappe.log_error(e, _('Failed to send {0} Auto Email Report').format(auto_email_report.name))