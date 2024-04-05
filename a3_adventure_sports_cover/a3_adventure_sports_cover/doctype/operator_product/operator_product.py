# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OperatorProduct(Document):
	def validate(self):
		for activity in self.activity_table:
			if activity.activity_name:
				act = frappe.get_doc("Operator Activity", activity.activity_name)
				for policy in act.activity_policy:
					if policy.insurance_policy:
						activity.insurance_policy = policy.insurance_policy
