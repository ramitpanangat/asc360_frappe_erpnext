# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.model.document import Document

class Booking(Document):
	def validate(self):
		if self.booking_date:
			date =  datetime.datetime.strptime(self.booking_date, "%Y-%m-%d")
			month = str(date.month)
			month_str = datetime.datetime.strptime(month, "%m")
			month_name = month_str.strftime("%b")
			self.month = month_name
			year = date.year
			self.year = year 

		if self.operator:
			if frappe.db.exists("Booking Summary",{"operator":self.operator,"month":self.month,"year":self.year}):
				summary = frappe.get_doc("Booking Summary",{"operator":self.operator,"month":self.month,"year":self.year})
				if summary.bookings:
					summary.append("bookings",{
						"booking_id": self.name,
						"operator_product": self.operator_product,
						"amount": self.total_amount
					})
				summary.save()
			else:
				summary = frappe.new_doc("Booking Summary")
				summary.operator = self.operator
				summary.month = self.month
				summary.year = self.year
				summary.append("bookings",{
					"booking_id": self.name,
					"operator_product": self.operator_product,
					"amount": self.total_amount
				})
				summary.insert()

