# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OnboardHospital(Document):
	def validate(self):
		if self.policy_number:
			policy = frappe.get_doc("Operator Policy Issued",self.policy_number)
			if policy.name1:
				self.policy_holder_name = policy.name1
