# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EVACEvent(Document):
	def validate(self):
		if self.onboard_vendor:
			vend = frappe.get_doc("Onboard Vendor",self.onboard_vendor)
			if vend.policy_holder_name:
				self.policy_holder_name = vend.policy_holder_name
