# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ListofPolicy(Document):
	pass
		# meta = frappe.get_meta("List of Policy")
		# fieldnames =[x.fieldname for x in meta.get("fields") if x.fieldtype in ["Data"]]
		# if fieldnames:
		# 	for d in fieldnames:
		# 		if self.get(d):
		# 			self.set(d, str(self.get(d)).upper())
					# self.get(d) = str(self.get(d)).upper()

