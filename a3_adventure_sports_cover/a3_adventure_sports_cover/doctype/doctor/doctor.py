# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe import new_doc
import frappe
from frappe.model.document import Document

class Doctor(Document):
	def after_insert(self):
		if not frappe.db.exists("User", {"email":self.email}):
			user = new_doc("User")
			user.first_name = self.doctor_name
			user.email = self.email
			user.phone = self.phone_number
			user.mobile_no = self.phone_number
			user.insert()
