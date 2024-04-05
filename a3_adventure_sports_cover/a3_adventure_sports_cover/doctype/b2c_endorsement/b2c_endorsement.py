# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class B2CEndorsement(Document):
	def on_submit(self):
		original_policy = frappe.get_doc("B2C Policy Issue", self.b2b_policy)
		en_policy = frappe.new_doc("B2C Policy Issue")
		en_policy.endorse = 1
		en_policy.endorsement = self.name
		en_policy.endorsement_count = int(original_policy.endorsement_count) + 1 if isinstance(original_policy.endorsement_count, str) else 1
		if original_policy.endorse == 0:
			en_policy.original_policy = self.b2b_policy
		else:
			en_policy.original_policy = original_policy.original_policy
		en_policy.policy = self.policy
		en_policy.policy_name = self.policy_name
		en_policy.customer_name = self.customer_name
		en_policy.invoice_and_payment = original_policy.invoice_and_payment
		en_policy.mode_of_payment = original_policy.mode_of_payment
		en_policy.account_paid_to = original_policy.account_paid_to
		en_policy.payment_id = self.payment_id
		en_policy.start_date = self.journey_start_date
		en_policy.end_date = self.journey_end_date
		en_policy.start_location = self.location_from
		en_policy.end_location = self.location_to
		en_policy.policy_type = "Single Policy"
		en_policy.submit()

		# Get document which we submitted above
		last_op = frappe.get_last_doc("B2C Policy Issue")

		# Compare previous and new B2B Policy Issued
		policy = frappe.get_doc("B2C Policy Issue", self.b2b_policy)
		old_op = policy.as_dict()
		new_op = last_op.as_dict()
		field_include = ["customer_name", "nationality", "nominee_name", "nominee_contact_number", "nominee_relationship", "premium", "end_date", "period_of_issuance", "policy", "start_date", "policy_provider","start_location","end_location"]
		datas = []
		for op in old_op:
			if old_op[op] != new_op[op] and op in field_include:
				data_sub = {}
				data_sub["field_name"] = op
				data_sub["old_value"] = old_op[op]
				data_sub["new_value"] = new_op[op]
				datas.append(data_sub)

		#Add Changed data to Endorsement Log
		endorse_log = frappe.new_doc("Endorsement Log")
		endorse_log.document = "B2C Policy Issue"
		endorse_log.policy = last_op.name
		endorse_log.endorsement_time = datetime.now()
		
		for data in datas:
			log = {}
			log["field_name"] = data["field_name"]
			log["old_value"] = data["old_value"] if data["old_value"] != None else "None"
			log["new_value"] = data["new_value"] if data["new_value"] != None else "None"
			log["datetime"] = datetime.now()
			endorse_log.append("log", log)
		endorse_log.insert()
