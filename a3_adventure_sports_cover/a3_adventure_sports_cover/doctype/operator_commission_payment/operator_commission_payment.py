# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from ast import operator
from dataclasses import fields
from enum import Flag
from frappe.model.document import Document
import frappe
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

class OperatorCommissionPayment(Document):
	def validate(self):
		operator_commission_list = frappe.get_list("Operator Commission Payable", filters={"operator":self.operator, "status":"Unpaid"}, fields=["name","operator","commission_payable"])
		commission = 0

		# Get list of dates between start-date and end-date
		sdate = datetime.strptime(self.period_start_date, "%Y-%m-%d").date()   # start date
		edate = datetime.strptime(self.period_end_date, "%Y-%m-%d").date()   # end date
		date_modified=sdate
		date_list=[sdate] 

		while date_modified<edate:
			date_modified+=timedelta(days=1) 
			date_list.append(date_modified)

		# Get all Operator Commission Payable of this operator between start date and end date
		self.operator_commission_payable.clear()
		for op_comm in operator_commission_list:
			op  = frappe.get_doc("Operator Commission Payable", op_comm.name)
			if op.policy_date in date_list:
				commission += op.commission_payable  # Get total commission to pay
				self.append("operator_commission_payable", {
					"operator_commission_payable": op.name,
					"commission": op.commission_payable
				})
		self.paid_amount = commission
		self.total_commission = commission
		
	def before_submit(self):
		if float(self.paid_amount) < 5000:
			payment_list = frappe.get_list("Operator Commission Payment",filters={"operator": self.operator, "status": "Rejected"})
			payment_list_paid = frappe.get_list("Operator Commission Payment",filters={"operator": self.operator, "status": "Paid"}, fields=["name", "paid_amount", "period_start_date"])
			today = datetime.now().date()
			paid = False
			potential_operator = False
			potential_list = []
			month_count = 1
			start_date = self.period_start_date
			end_date = self.period_end_date

			# Check if start date and end date are string or datetime and convert it to datetime
			if isinstance(start_date, str):
				start_date = datetime.strptime(start_date, "%Y-%m-%d")
				
			if isinstance(end_date, str):
				end_date = datetime.strptime(end_date, "%Y-%m-%d")

			# Check if the operator is a potential operator or not
			while month_count <= 6:
				#Minus one month from after a loop and check if total commission is equal to or greater than 5000 for 6 months
				sdate = datetime(start_date.year, start_date.month-month_count, 1)   #first date of the month
				edate = datetime(end_date.year, end_date.month-month_count, 1) + relativedelta(day=31)   #Last date of the month
				date_modified=sdate
				date_list=[sdate] 
				total_commission = 0

				# get all dates between two start date and end date
				while date_modified<edate:
					date_modified+=timedelta(days=1)
					date_list.append(date_modified)

				# If period_start_date is the date_list it will add paid amount to total_commission variable
				for payment_paid in payment_list_paid:
					if payment_paid.period_start_date in date_list:
						total_commission += payment_paid.paid_amount
				if total_commission >= 5000:
					potential_list.append(True)
				
				month_count += 1

			# if any of the month had total commission below 5000 this operator will not be considered as potential operator
			if False not in potential_list:
				potential_operator = True

			if len(payment_list)>0:
				for pay_list in payment_list:
					pay_list_doc = frappe.get_doc("Operator Commission Payment", pay_list.name)
					no_month = (today.year - pay_list_doc.request_date.year) * 12 + today.month - pay_list_doc.request_date.month
					if potential_operator == True:
						if isinstance(self.request_date, str):
							request_date = datetime.strptime(self.request_date, "%Y-%m-%d").date()
						else:
							request_date = self.request_date
						no_days = today - request_date
						if abs(no_days.days) >= 15:
							paid = True
						else:
							paid = False
					else:
						if int(no_month) < 3:
							paid = False
						else:
							paid = True
				if paid == True:
					self.status = "Paid"
				else:
					self.status = "Rejected"
			else:
				self.status = "Rejected"
		else:
			self.status = "Paid"
		self.posting_date = datetime.today().date()

	def on_submit(self):
		if self.status == "Paid":
			for commission in self.operator_commission_payable:
				ocp = frappe.get_doc("Operator Commission Payable", commission.operator_commission_payable)
				ocp.status = "Paid"
				ocp.save()
			# Create Payement entry for each Operator Commission Payable
			payment_entry = frappe.new_doc("Payment Entry")
			payment_entry.payment_type = self.payment_type
			payment_entry.posting_date = self.posting_date
			payment_entry.mode_of_payment = self.mode_of_payment
			payment_entry.party_type = "Supplier"
			payment_entry.party = self.operator
			payment_entry.party_data = self.operator
			payment_entry.party_name = self.operator
			payment_entry.paid_amount = self.paid_amount
			payment_entry.received_amount = self.paid_amount
			payment_entry.paid_from = self.paid_from
			payment_entry.reference_no = self.reference_no
			payment_entry.reference_date = self.reference_date
			payment_entry.submit()
		else:
			frappe.msgprint("Your commission is less than 5000. Please request after 3 months.")