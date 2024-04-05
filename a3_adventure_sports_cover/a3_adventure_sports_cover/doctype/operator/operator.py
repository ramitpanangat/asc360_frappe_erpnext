# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe import get_doc, msgprint, db, new_doc

class Operator(Document):
	def validate(self):
		
		if self.added_by_agent == "Yes":
			if not self.agent_name:
				frappe.throw("Please enter the Agent Name.")

	def after_insert(self):
		
		# Create Operator User
		user = get_doc({
			"doctype": "User",
			"first_name": self.operator_name,
			"email": self.email,
			"user_type": "Website User",
			"send_welcome_email": 0,
			"role_profile_name": "Operator Roles"
    	})
		user.insert()

		# Create Operator Customer 
		address = ""
		if self.address:
			address = self.address
		customer = get_doc({
			"doctype": "Customer",
			"customer_name": self.operator_name,
			"customer_group": "Operator Customer",
			"territory": self.territory,
		})
		customer.insert()
		self.customer_name = customer.name

		#Create Contact
		contact = new_doc("Contact")
		contact.first_name = customer.name
		contact.append("email_ids", {
			"email_id": self.email,
			"is_primary": 1
		})
		contact.insert()
		self.contact = contact.name
		customer.customer_primary_contact = contact.name
		customer.save()

		# Create Operator Sales Partner
		commission = 0
		if self.commission_percentage:
			commission = self.commission_percentage

		partner = get_doc({
			"doctype": "Sales Partner",
			"partner_name": self.operator_name,
			"territory": self.territory,
			"commission_rate": commission,
			"partner_type": "Operator Sales Partner"
		})
		partner.insert()
		self.sales_partner_id = partner.name

		# Create Operator Supplier
		supplier = get_doc({
			"doctype": "Supplier",
			"supplier_name": self.operator_name,
			"supplier_group": "Operator Supplier"
		})
		supplier.insert()
		self.supplier = supplier.name

		# Create Agent Commission Payable if added by Agent
		if self.added_by_agent == "Yes":
			agent = get_doc("Agents", self.agent_name)

			if agent.op_commission_type == "Amount":
				commission = agent.op_commission_amount
			else:
				commission = 0

		if self.added_by_agent == "Yes":
			com = frappe.new_doc("Agent Commission Payable")
			com.agent = self.agent_name
			com.policy = "B2B Policy Issue"
			com.status = "Pending Approval"
			# com.policy_number = policy_doc.name
			com.policy_date = datetime.today().date()
			com.commission_payable = commission 
			com.insert()
		
		success_message = """
		<span>Operator Created Successfully. Following documents are also created.</span>
		<ol>
		<li>User</li>
		<li>Customer</li>
		<li>Sales Partner</li>
		<li>Supplier</li>
		<ol>
		"""
		msgprint(success_message, as_list=True)
		self.save()