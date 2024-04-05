# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class B2CPolicyQueue(Document):
	def validate(self):
		if len(self.policy_list)==0:
			self.no_of_batches = 0
