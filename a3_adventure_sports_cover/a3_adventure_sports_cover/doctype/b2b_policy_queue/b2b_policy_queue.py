# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class B2BPolicyQueue(Document):
	def validate(self):
		count = 0
		for detail in self.customer_details:
			if detail.priority_ranking > count:
				count = detail.priority_ranking
		self.no_of_policies = count
		
		if len(self.customer_details) == 0:
			self.last_updated_batch = 0
			self.no_of_policies = 0
			self.index = 0
