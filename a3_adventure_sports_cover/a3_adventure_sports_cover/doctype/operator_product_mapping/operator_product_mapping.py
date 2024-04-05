# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

from warnings import filters
import frappe
from frappe.model.document import Document

class OperatorProductMapping(Document):
	def validate(self):
		if frappe.db.exists("Operator Product Mapping", {"operator": self.operator, "policy": self.policy}):
			frappe.throw(f"The Customised Policy '{self.policy}' is already assigned to the operator '{self.operator}'.")

