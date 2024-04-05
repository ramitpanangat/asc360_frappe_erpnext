# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe import get_doc, get_last_doc, get_value, new_doc
from datetime import datetime

class EndorsementForm(Document):
	def on_submit(self):
		endorsed = get_doc("Operator Policy Issued", self.policy_detail)
		operator_policy = new_doc("Operator Policy Issued")
		operator_policy.endorsed = 1
		operator_policy.endorsement = self.name
		if endorsed.endorsed==0:
			operator_policy.original_policy = self.policy_detail
			operator_policy.endorsement_count = 1
		else:
			operator_policy.original_policy = endorsed.original_policy
			operator_policy.endorsement_count = int(endorsed.endorsement_count) + 1
		operator_policy.operator = self.operator
		operator_policy.batch_id = self.batch_id
		operator_policy.supplier_policy_id= self.supplier_policy_id
		operator_policy.policy_number = self.policy_number
		operator_policy.date_of_issue = self.date_of_issue
		operator_policy.status = self.status
		operator_policy.name1 = self.name1
		operator_policy.gender = self.gender
		operator_policy.email_id = self.email_id
		operator_policy.address = self.address
		operator_policy.pan_number = self.pan_number
		operator_policy.dob = self.dob
		operator_policy.nationality = self.nationality
		operator_policy.contact = self.contact
		operator_policy.aadhaar_number = self.aadhaar_number
		operator_policy.passport_number = self.passport_number
		operator_policy.nominee_name = self.nominee_name
		operator_policy.nominee_contact_number = self.nominee_contact_number
		operator_policy.nominee_relationship = self.nominee_relationship
		operator_policy.operator_product = self.operator_product
		operator_policy.booking_date = self.booking_date
		operator_policy.nature_of_activity = self.nature_of_activity
		operator_policy.any_previous_insurance_ever_been_declined = self.any_previous_insurance_ever_been_declined
		operator_policy.time_of_day_of_activity = self.time_of_day_of_activity
		operator_policy.activity_date = self.activity_date
		operator_policy.doctor_or_medical_practitioner_on_site = self.doctor_or_medical_practitioner_on_site
		operator_policy.manager_or_trainer_to_group_members_ratio = self.manager_or_trainer_to_group_members_ratio
		operator_policy.activity = self.activity
		operator_policy.premium = self.premium
		operator_policy.end_date = self.end_date
		operator_policy.period_of_issuance = self.period_of_issuance
		operator_policy.policy = self.policy
		operator_policy.start_date = self.start_date
		operator_policy.policy_provider = self.policy_provider
		operator_policy.submit()

		# Get document which we submitted above
		last_op = get_last_doc("Operator Policy Issued")
		
		# Compare previous and new Operator Policy Issued
		old_op = endorsed.as_dict()
		new_op = last_op.as_dict()
		field_include = ["name1", "gender", "email_id", "address", "pan_number", "dob", "nationality", "contact", "aadhaar_number", "passport_number", "nominee_name", "nominee_contact_number", "nominee_relationship", "activity", "premium", "end_date", "period_of_issuance", "policy", "start_date", "policy_provider"]
		datas = []
		for op in old_op:
			if old_op[op] != new_op[op] and op in field_include:
				data_sub = {}
				data_sub["field_name"] = op
				data_sub["old_value"] = old_op[op]
				data_sub["new_value"] = new_op[op]
				datas.append(data_sub)

		#Add Changed data to Endorsement Log
		endorse_log = new_doc("Endorsement Log")
		endorse_log.document = "Operator Policy Issued"
		endorse_log.policy = last_op.name
		endorse_log.endorsement_time = datetime.now()
		
		for data in datas:
			endorse_log.append("log", {
				"field_name": data["field_name"],
				"old_value": data["old_value"],
				"new_value": data["new_value"],
				"datetime": datetime.now()
			})
			
		endorse_log.insert()

