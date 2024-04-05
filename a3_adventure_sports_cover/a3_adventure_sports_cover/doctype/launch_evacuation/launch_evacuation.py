# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaunchEvacuation(Document):
	def validate(self):
		if self.onboard_vendor:
			vend = frappe.get_doc("Onboard Vendor",self.onboard_vendor)
			if vend.connection_status:
				self.connection_status = vend.connection_status
		if self.incident_number:
			incident = frappe.get_doc("Incident Report",self.incident_number)
			if incident.caller_name:
				self.name_of_caller = incident.caller_name
			if incident.caller_contact_number:
				self.caller_contact = incident.caller_contact_number
			if incident.relation_to_claimaint:
				self.relation_to_claimaint = incident.relation_to_claimaint
			if incident.hamrc_id:
				self.membership_id = incident.hamrc_id
