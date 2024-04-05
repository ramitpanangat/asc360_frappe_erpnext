# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OnboardVendor(Document):
	def validate(self):
		if self.doctor_onboarding:
			doc_on = frappe.get_doc("Doctor On Boarding",self.doctor_onboarding)
			if doc_on.connection_status:
				self.connection_status = doc_on.connection_status
