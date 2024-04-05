# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OperatorActivity(Document):
	def validate(self):
		for activity in self.activity_policy:
			if activity.insurance_policy:
				act = frappe.get_doc("Item",activity.insurance_policy)
				price = act.standard_rate
				activity.premium_amount = price
