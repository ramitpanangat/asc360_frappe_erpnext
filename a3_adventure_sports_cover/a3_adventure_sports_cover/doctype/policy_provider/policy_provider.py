# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe import new_doc
from frappe.model.document import Document

class PolicyProvider(Document):
	def after_insert(self):
		supplier = new_doc("Supplier")
		supplier.supplier_name = self.policy_provider
		supplier.country = self.country
		supplier.supplier_group = "Insurance Provider"
		supplier.default_bank_account = self.default_company_bank_account
		supplier.tax_id = self.tax_id
		supplier.tax_withholding_category = self.tax_withholding_category
		supplier.supplier_type = self.policy_provider_type
		supplier.pan = self.pan
		supplier.tax_category = self.tax_categry
		supplier.insert()