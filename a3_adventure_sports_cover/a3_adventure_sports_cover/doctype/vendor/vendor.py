# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class Vendor(Document):
	def after_insert(self):
		if not frappe.db.exists("Supplier", self.vendor_name):
			supplier = frappe.new_doc("Supplier")
			supplier.supplier_name = self.vendor_name
			supplier.supplier_group = "Vendor Supplier"
			supplier.insert()
