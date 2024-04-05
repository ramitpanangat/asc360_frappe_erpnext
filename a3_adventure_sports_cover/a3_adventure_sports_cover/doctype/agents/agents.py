# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe import get_doc

class Agents(Document):
	def after_insert(self):
		# Create Operator User
		user = get_doc({
			"doctype": "User",
			"first_name": self.agent_name,
			"email": self.agent_email,
			"user_type": "Website User",
			"send_welcome_email": 0
    	})
		user.insert()

		# Create Operator Customer 
		contact = ""
		if self.phone_number:
			contact = self.phone_number
		customer = get_doc({
			"doctype": "Customer",
			"customer_name": self.agent_name,
			"customer_group": "Agent Customer",
			"territory": self.territory,
			"customer_primary_contact": contact,
		})
		customer.insert()
		self.customer_id = customer.name

		# Create Operator Sales Partner
		commission = 0
		if self.commission_percentage:
			commission = self.commission_percentage

		partner = get_doc({
			"doctype": "Sales Partner",
			"partner_name": self.agent_name,
			"territory": self.territory,
			"commission_rate": commission,
			"partner_type": "Agent Sales Partner"
		})
		partner.insert()
		self.sales_partner_id = partner.name

		# Create Operator Supplier
		supplier = get_doc({
			"doctype": "Supplier",
			"supplier_name": self.agent_name,
			"supplier_group": "Agent Supplier"
		})
		supplier.insert()
		self.supplier_id = supplier.name

		self.save()
