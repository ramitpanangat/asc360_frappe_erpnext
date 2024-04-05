# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PreCheckup(Document):
	def validate(self):
		if self.onboard_hospital:
			hosp = frappe.get_doc("Onboard Hospital",self.onboard_hospital)
			if hosp.policy_holder_name:
				self.customer_name = hosp.policy_holder_name
			if hosp.launch_evacuation:
				evac = frappe.get_doc("Launch Evacuation", hosp.launch_evacuation)
				if evac.membership_id:
					self.membership_id = evac.membership_id
