# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ActivityMaster(Document):
	def validate(self):
		for level in self.levels_of_activity:
			if level.policy_provider == "HDFC":
				self.hdfc_level = level.level
			if level.policy_provider == "ICICI Lombard":
				self.icici_level = level.level
