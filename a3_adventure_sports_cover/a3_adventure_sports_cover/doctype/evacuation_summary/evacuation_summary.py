# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EvacuationSummary(Document):
	def validate(self):
		if self.incident_number:
			incident = frappe.get_doc("Incident Report",self.incident_number)
			# if incident.policy_holder:
			# 	self.policy_holder_name = incident.policy_holder
			if incident.caller_name:
				self.caller_name = incident.caller_name
			if incident.caller_contact_number:
				self.caller_contact = incident.caller_contact_number
			if incident.relation_to_claimaint:
				self.relation_to_claimaint = incident.relation_to_claimaint
			if incident.evacuation_incharge:
				self.evacuation_incharge = incident.evacuation_incharge
			if frappe.db.exists("Onboard Hospital", self.incident_number):
				hosp = frappe.get_doc("Onboard Hospital", self.incident_number)
				if hosp.hospital:
					self.hospital = hosp.hospital
			if frappe.db.exists("Doctor On Boarding",self.incident_number):
				doct = frappe.get_doc("Doctor On Boarding",self.incident_number)
				if doct.evacuation_type:
					self.evacuation_type = doct.evacuation_type
				if doct.evacuation_priority:
					self.evacuation_priority - doct.evacuation_priority
				if doct.doctor:
					self.doctor_attended = doct.doctor
				
		if self.policy_number:
			policy = frappe.get_doc("Operator Policy Issued",self.policy_number)
			if policy.supplier_policy_id:
				self.supplier_policy_number = policy.supplier_policy_id
			if policy.name1:
				self.policy_holder_name = policy.name1
