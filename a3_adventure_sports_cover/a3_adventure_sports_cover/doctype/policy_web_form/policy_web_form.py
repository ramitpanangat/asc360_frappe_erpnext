# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PolicyWebForm(Document):
	def after_insert(self):
		customer = self.customer
		doi = self.date_of_issue
		dob = self.date_of_birth
		operator = self.operator
		policy = self.policy
		start_date = self.beginning_date
		if self.customer:
			issue_policy = frappe.new_doc("Issue Policy")
			issue_policy.customer = customer
			issue_policy.date_of_birth = dob 
			issue_policy.date_of_issue = doi 
			issue_policy.operator = operator
			issue_policy.policy = policy 
			issue_policy.beginning_date = start_date 
			issue_policy.submit()
