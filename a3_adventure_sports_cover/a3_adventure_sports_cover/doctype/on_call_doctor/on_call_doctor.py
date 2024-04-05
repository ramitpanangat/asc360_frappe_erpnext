# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OnCallDoctor(Document):
	def validate(self):
		if self.policy_number:
			policy = frappe.get_doc("Operator Policy Issued",self.policy_number)
			if policy.name1:
				self.policy_holder = policy.name1
		
		if self.on_call_doctors:
			for row in self.on_call_doctors:
				if row.doctor:
					doc = frappe.get_doc("Doctor",row.doctor)
					if doc.doctor_id:
						row.doctor_id = doc.doctor_id
					if doc.location:
						row.location = doc.location
					if doc.date_of_birth:
						row.date_of_birth = doc.date_of_birth
