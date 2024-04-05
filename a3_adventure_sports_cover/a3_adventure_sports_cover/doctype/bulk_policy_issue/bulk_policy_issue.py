# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe import get_value, new_doc, get_doc, db, sendmail
from frappe.model.document import Document

class BulkPolicyIssue(Document):

	def validate(self):
		customer_details = self.bulk_policy_issue
		for cust in self.bulk_policy_issue:
			print(cust.name1)
			print(db.exists("Customer", cust.name1))
			if not db.exists("Customer", cust.name1):
				customer = new_doc("Customer")
				customer.customer_name = cust.name1
				customer.customer_group = "All Customer Groups"
				customer.territory = "All Territories"
				customer.insert()
			
	
	def on_submit(self):
		customer_details = self.bulk_policy_issue
		item = get_doc("Item", self.policy)

		for customer in customer_details:
			op = get_value("Operator", self.operator, "email")
			operator_policy_issued = new_doc("B2B Policy Issue")
			operator_policy_issued.policy_type = "Single Policy"
			operator_policy_issued.operator = self.operator
			operator_policy_issued.operator_email = op
			# operator_policy_issued.status = "Issued"
			operator_policy_issued.start_date = self.start_date
			operator_policy_issued.end_date = self.end_date_2
			# operator_policy_issued.operator_product = self.operator_product
			# operator_policy_issued.activity = self.operator_product
			operator_policy_issued.policy = self.policy
			operator_policy_issued.amount = item.standard_rate
			operator_policy_issued.policy_provider = self.policy_provider
			operator_policy_issued.customer_name = customer.name1
			operator_policy_issued.gender = customer.gender
			operator_policy_issued.date_of_birth = customer.date_of_birth
			operator_policy_issued.email_id = customer.email_id
			operator_policy_issued.phone_number = customer.contact
			operator_policy_issued.address = customer.address
			operator_policy_issued.nationality = customer.nationality
			operator_policy_issued.pan_number = customer.pan_number
			operator_policy_issued.aadhar_number = customer.aadhar_number
			operator_policy_issued.passport_number = customer.passport_number
			operator_policy_issued.nominee_name = customer.nominee_name
			operator_policy_issued.nominee_contact_number = customer.nominee_contact
			operator_policy_issued.nominee_relationship = customer.nominee_relationship
			operator_policy_issued.policy_name = item.parent_policy
			operator_policy_issued.save()
			operator_policy_issued.submit()
