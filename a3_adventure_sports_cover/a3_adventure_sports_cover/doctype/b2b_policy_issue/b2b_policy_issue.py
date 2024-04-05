# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from datetime import datetime as dt
from a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events import send_whatsapp_notification
import frappe
import random
from re import fullmatch


class B2BPolicyIssue(Document):
	def before_insert(self):

		self.policy_list.clear()
		#Naming Series
		if self.policy_type == "Single Policy":
			if self.endorsed == 0:
				scope_id = ""
				type_id = ""
				provider_id = ""
				operator_id = ""
				operator_code = ""

				if self.policy:
					pol = frappe.get_doc("Item",self.policy)
					if pol.master_policy:
						master = frappe.get_doc("Policy Master",pol.master_policy)
						if master.scope_of_policy:
							scope = master.scope_of_policy
							if scope == "International":
								scope_id = "I"
							elif scope == "Domestic":
								scope_id = "D"
						if master.type_of_policy:
							type = master.type_of_policy
							if type == "Short Term":
								type_id = "S"
							elif type == "Annual":
								type_id = "A"
						if master.policy_provider:
							provider = master.policy_provider
							provider_id = provider[0]

				if self.policy_issued_by == "Operator":
					operator_code = frappe.get_value("Operator", self.operator, "operator_code")
				if self.policy_issued_by == "Agent":
					operator_code = frappe.get_value("Agents", self.agent_name, "agent_code")

				if operator_code:
					operator_id = operator_code
							
				today = dt.today()
				policy_list = frappe.get_list("List of Policy")
				
				if len(policy_list) == 0:
					series_no = 0
				else:
					last_doc = frappe.get_last_doc("List of Policy")
					series_no = int(last_doc.series_number)+1

				if scope_id!="" and type_id!="" and provider and operator_id:
					policy_number = f"ASC360-{scope_id}{type_id}{provider_id}{operator_id}-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"
				else:
					policy_number = f"ASC360-MDBK-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"

				self.policy_number = policy_number
			else:
				self.policy_number = f"{self.original_policy} - {self.endorsemnet_count}"
		else:
			policy_list = frappe.get_list("Bulk Policy Series Number")
			if len(policy_list) == 0:
				series_no = 0
			else:
				last_doc = frappe.get_last_doc("Bulk Policy Series Number")
				series_no = int(last_doc.series_number)+1
			today = dt.today()
			self.bulk_policy_number = f"BU-{today.month}-{today.year}-{'{:05d}'.format(series_no)}"
			self.policy_number = f"BU-{today.month}-{today.year}-{'{:05d}'.format(series_no)}"
	
	def after_insert(self):
		# Seb - Templates Fetching
		if self.policy_name:
			pol_nam = frappe.get_doc("Customised Policy", self.policy_name)
			if pol_nam.parent_policy:
				moth_pol = frappe.get_doc("Policy Master", pol_nam.parent_policy)
				if moth_pol.why_asc :
					for rows in moth_pol.why_asc:
						self.append("why_asc", {
						"why_asc": rows.why_asc
					})
				if moth_pol.footer :
					for row in moth_pol.footer:
						self.append("footer", {
						"footer_content": row.footer_content
					})
				if moth_pol.please_note :
					for lines in moth_pol.please_note:
						self.append("please_note", {
						"note_template": lines.note_template
					})
				if moth_pol.claim_procedure :
					for cla in moth_pol.claim_procedure:
						self.append("claim_procedure", {
						"claim_procedure": cla.claim_procedure 
					})
				if moth_pol.important_note :
					for imp in moth_pol.important_note:
						self.append("important_note", {
						"important_note": imp.important_note
					})
				

				
		#PNR Number
		if not self.pnr_number:
			pnr = random.randint(10000000,99999999)
			new_pnr = frappe.new_doc("PNR Number")
			new_pnr.pnr = pnr 
			new_pnr.insert()
			self.pnr_number = new_pnr.name
		self.save()

		
		#Adding policy List Of Policy Doctype
		if self.policy_type == "Single Policy":
			policy_list = frappe.get_list("List of Policy")
			if len(policy_list)==0:
				series_no = 0
			else:
				last_doc = frappe.get_last_doc("List of Policy")
				series_no = int(last_doc.series_number)+1
			list_of_policy = frappe.new_doc("List of Policy")
			list_of_policy.document = "B2B Policy Issue"
			list_of_policy.batch_id = self.batch_id
			list_of_policy.policy = self.policy_number
			list_of_policy.policy_added_by =self.policy_issued_by
			if self.policy_issued_by == "Operator":
				list_of_policy.operator = self.operator
			elif self.policy_issued_by == "Agent":
				list_of_policy.agent = self.agent_name
			list_of_policy.start_date = self.start_date
			list_of_policy.end_date = self.end_date
			list_of_policy.series_number = series_no
			list_of_policy.customer = self.customer_name
			list_of_policy.date_of_birth = self.date_of_birth
			list_of_policy.period_of_issuance = self.period_of_issuance 
			list_of_policy.amount = self.amount
			list_of_policy.policy_provider = self.policy_provider
			list_of_policy.date_of_issue = self.date_of_issue
			list_of_policy.insert()

			if self.external_source == "Yes":
				self.submit()
		else:
			bulk_series_list = frappe.get_list("Bulk Policy Series Number")
			if len(bulk_series_list) == 0:
				series_no = 0
			else:
				last_doc = frappe.get_last_doc("Bulk Policy Series Number")
				series_no = int(last_doc.series_number)+1
			bulk_series = frappe.new_doc("Bulk Policy Series Number")
			bulk_series.series_number = series_no
			bulk_series.insert()



	def on_submit(self):
		#Validate Operator Balance
		if self.policy_issued_by == "Operator":
			if self.policy_type == "Bulk Policy":
				prem = self.amount
				row = len(self.bulk_upload)
				total = float(prem) * float(row) 
				bal = self.operator_balance
				if total>bal:
					frappe.throw("Operator Balance Not Enough to Issue Policies!!")
			elif self.policy_type == "Single Policy":
				if not self.batch_id:
					prem = self.amount
					bal = self.operator_balance
					# print("Yaha", bal, prem)
					if prem>bal:
						frappe.throw("Operator Balance Not Enough to Issue Policy!!")
		frappe.msgprint("Sales Invoice generated & Submitted successfully")
		
		# #Validate Start Date !< Today
		today = self.date_of_issue
		start = self.start_date
		if isinstance(today, str):
			today = dt.strptime(self.date_of_issue, "%Y-%m-%d").date()
		if isinstance(start, str):
			start = dt.strptime(self.start_date, "%Y-%m-%d").date()
		r = (start - today)
		days = r.days + 1   #to rectify today-today = -1
		if self.admin_approved == 0:
			if days < 0:
				frappe.throw("Start Date Has to be Greater than or Equal to Date of Issue.")

		# #Validate End Date !< Start Date
		end = self.end_date
		if isinstance(end, str):
			end = dt.strptime(self.end_date, "%Y-%m-%d").date()
			
		if end < start:
			frappe.throw("End Date cannot be Before Start Date!")

		#Update Operator Balance
		if self.policy_type == "Single Policy":
			if self.policy_issued_by == "Operator":
				if self.operator:
					self.operator_balance_check()
					if self.has_membership == "Yes":
						self.check_membership()
			
			self.create_invoice(self.policy_issued_by)
			self.create_commission_payable()
			# attach_pdf(self)

		#Insert Policy for Bulk Upload
		if self.policy_type == "Bulk Policy":
			if self.bulk_upload:
				email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

				customer_details = self.bulk_upload
				queue_doc = frappe.get_single("B2B Policy Queue")
				for cust in customer_details:

					queue_doc.append("customer_details", {
						"priority_ranking": queue_doc.no_of_policies + 1,
						"main_policy": self.name,
						"customer_name": str(cust.name1).strip(),
						"gender": cust.gender,
						"date_of_birth": cust.date_of_birth,
						"email_id": cust.email_id,
						"contact": cust.contact,
						"address": cust.address,
						"event": cust.event,
						"pan_number": cust.pan_number,
						"aadhar_number": cust.aadhar_number,
						"passport_number": cust.passport_number,
						"nominee_name": cust.nominee_name,
						"nominee_contact": cust.nominee_contact,
						"nominee_relationship": cust.nominee_relationship,
						"admin_approved": self.admin_approved
					})

				queue_doc.no_of_policies += 1
				queue_doc.save()


	def validate(self):
							
		if self.policy_type == "Single Policy":
			if self.name_of_customer:
				if not self.customer_name:
					if not frappe.db.exists("Customer", {"customer_name": str(self.name_of_customer).strip(), "email_id": self.email_id.strip(), "mobile_no": self.phone_number.strip()}):
						date_of_birth = self.date_of_birth
						if isinstance(date_of_birth, str):
							date_of_birth = dt.strptime(date_of_birth, "%Y-%m-%d").date()
						customer = frappe.new_doc("Customer")
						customer.customer_name = self.name_of_customer
						customer.customer_type = "Individual"
						customer.customer_group = "Individual"
						customer.date_of_birth = date_of_birth
						customer.gender = self.gender
						customer.territory = "India"
						customer.insert()

						if self.email_id or self.phone_number:
							contact = frappe.new_doc("Contact")
							contact.first_name = self.name_of_customer
							contact.gender = self.gender
							if self.email_id:
								contact.append("email_ids",{
									"email_id": self.email_id,
									"is_primary": 1
								})
							if self.phone_number:
								contact.append("phone_nos",{
									"phone": self.phone_number,
									"is_primary_phone": 1,
									"is_primary_mobile_no": 1
								})
							contact.append("links",{
								"link_doctype": "Customer",
								"link_name": customer.name,
								"link_title": customer.name
							})
							contact.insert()
							customer.customer_primary_contact = contact.name
							customer.save()
						self.customer_name = customer.name
					else:
						self.customer_name = frappe.get_doc("Customer", {"customer_name": self.name_of_customer, "email_id": self.email_id, "mobile_no": self.phone_number}).name
			else:
				if self.customer_name:
					self.name_of_customer = frappe.get_value("Customer", self.customer_name, "customer_name")

		self.created_on = self.creation
		if self.docstatus == 0:
			if self.pdf_added != "In Process":
				self.pdf_added = "In Process"

		self.custom_policy = frappe.get_doc("Customised Policy", self.policy_name)
		if self.custom_policy.select_the_template:
					self.select_the_template = self.custom_policy.select_the_template
		if self.custom_policy.description:
			self.terms_and_conditions = self.custom_policy.description
		self.activity_list.clear()

		# Fetch activities from Customised Policy
		if self.docstatus == 0:
			for activities in self.custom_policy.activity_list:
				activity = frappe.get_doc("Activity Master", activities.activity_name)
				if activity.prime_activity == "Yes":
					self.append("activity_list", {
						"activity_name": activity.activity_name,
						"level": activity.activity_level
					})
		
		# if self.date_of_birth:
		# 	date_of_issue = dt.strptime(self.date_of_issue, "%Y-%m-%d").date()
		# 	date_of_birth = dt.strptime(str(self.date_of_birth), "%Y-%m-%d").date()
		# 	diff = date_of_issue - date_of_birth
		# 	if date_of_issue < date_of_birth or diff.days < 366:
		# 		frappe.throw("Invalid Date of Birth")

		if self.policy_issued_by == "Operator":
			bal = frappe.get_value("Operator Balance", self.operator, "balance_available")
			if bal:
				self.operator_balance = bal
			else:
				self.operator_balance = 0

		#Fetch Activities From Master
		activity_list = []
		if self.policy_name:
			if self.custom_policy.activity_list:
				for row in self.custom_policy.activity_list:
					activity_list.append(row.activity_name)
				# print(activity_list)
				a= ""
				for activity in activity_list:
					a = a + activity + ","
				self.adventure_sports_activities_on_trip = a

		if self.policy_type == "Single Policy":
			self.validate_customer_details(self.customer_name, self.email_id, self.phone_number, self.date_of_birth)

			if self.customer_name:
				customer = frappe.get_doc("Customer",self.customer_name)
				if customer.date_of_birth:
					self.date_of_birth = customer.date_of_birth
				if customer.gender:
					self.gender = customer.gender
				if customer.mobile_no:
					self.phone_number = customer.mobile_no
				if customer.email_id:
					self.email_id = customer.email_id
				if customer.customer_primary_address:
					address = frappe.get_doc("Address",customer.customer_primary_address)
					if address.address_line1:
						self.address_line_1 = address.address_line1
					if address.address_line2:
						self.address_line_2 = address.address_line2
					if address.city:
						self.city = address.city
					if address.state:
						self.state = address.state
					if address.country:
						self.country = address.country
					if address.pincode:
						self.pin_code = address.pincode

			if self.exchange_rate:
				converted_amount = self.amount * self.exchange_rate
				self.premium_in_inr = converted_amount

		elif self.policy_type == "Bulk Policy":
			if self.bulk_upload:
				for cust in self.bulk_upload:
					self.validate_customer_details(cust.name1, cust.email_id, cust.contact, cust.date_of_birth)
					
			if self.exchange_rate:
				if len(self.bulk_upload)>0:
					converted_amount = self.amount * self.exchange_rate
					self.premium_in_inr = converted_amount * len(self.bulk_upload)
				else:
					self.premium_in_inr = 0

		if self.policy:
			item_price = frappe.get_doc("Item Price",{"item_code":self.policy})
			if item_price.currency:
				self.premiun_currency = item_price.currency
	
	def create_invoice(self, policy_issued_by):
		today = dt.now().date()
		invoice = frappe.new_doc("Sales Invoice")
		invoice.customer = self.customer_name
		invoice.policy_number = self.name
		invoice.due_date = self.date_of_issue
		if policy_issued_by == "Operator":
			invoice.operator = self.operator
			invoice.sales_partner = self.operator
		else:
			invoice.agent = self.agent_name
			invoice.sales_partner = self.agent_name
		invoice.append(
			"items",
			{
				"item_code": self.policy,
				"rate": self.premium_in_inr
			},
		)
		invoice.set_missing_values()
		invoice.insert()
		invoice.submit()

		payment_entry = frappe.new_doc("Payment Entry")
		payment_entry.payment_type = "Receive"
		payment_entry.posting_date = today
		payment_entry.mode_of_payment = "Cash"
		payment_entry.paid_to = "Cash - ASC"
		payment_entry.party_type = "Customer"
		payment_entry.policy_number = self.name
		payment_entry.party = self.customer_name
		payment_entry.party_data = self.customer_name
		payment_entry.party_name = self.customer_name
		payment_entry.paid_amount = self.premium_in_inr
		payment_entry.received_amount = self.premium_in_inr
		payment_entry.target_exchange_rate = self.exchange_rate
		payment_entry.insert()
		payment_entry.submit()

		invoice.status = "Paid"
		invoice.db_update()

	def operator_balance_check(self):
		op = self.operator
		if frappe.db.exists("Operator Balance",op):
			bal = frappe.get_doc("Operator Balance",op)
			if bal.number_of_policy_issued:
				no = float(bal.number_of_policy_issued)
				nos = no + 1
				bals = bal.balance_available
				bal.number_of_policy_issued = float(nos)
				bal.total_policy_amount += self.amount 
				bal.balance_available = float(bals) - float(self.amount)
				bal.save()
			else:
				bal.number_of_policy_issued =1
				bal.total_policy_amount += self.amount 
				bal.balance_available = bal.invoice_amount - bal.total_policy_amount
				bal.save()

	def on_cancel(self):
		operator_balance = frappe.get_doc("Operator Balance", self.operator)
		operator_balance.balance_available += self.amount
		operator_balance.total_policy_amount -= self.amount
		operator_balance.save()
		send_whatsapp_notification(self, alert_on="Cancel")

	
	def check_membership(self):
		if self.has_membership == "Yes":
			membership_issue = frappe.get_doc("Membership Issuance", self.membership_id)
			membership_issue.append("activities_list", {
				"type_of_policy": self.doctype,
				"policy_number": self.name,
				"amount": self.premium_in_inr,
				"activity_date": self.date_of_issue
			})
			balance = membership_issue.balance_available
			for activity in membership_issue.activities_list:
				balance -= activity.amount
			membership_issue.balance_available = balance
			membership_issue.save()
			membership_issue.db_update()
	
	def create_commission_payable(self):
		if self.policy_issued_by == "Operator":
			operator = frappe.get_doc("Operator", self.operator)
			if operator.commisson_type:
				if operator.commisson_type == "Percentage":
					if operator.commission_percentage:
						perc = operator.commission_percentage

						#Calculate Commission
						amount = self.amount
						commission = (amount * perc)/100
						#Insert Operator Commission Receivable
						if commission:
							if not frappe.db.exists("Operator Commission Payable", {"policy_number": self.name}):
								com = frappe.new_doc("Operator Commission Payable")
								com.operator = self.operator
								com.policy = "B2B Policy Issue"
								com.status = "Unpaid"
								com.policy_number = self.name
								com.policy_date = self.date_of_issue
								com.commission_payable = commission 
								com.insert()
				elif operator.commisson_type == "Amount":
					if operator.commission_amount:

						#Calculate Commission
						commission = operator.commission_amount
						#Insert Operator Commission Receivable

						if not frappe.db.exists("Operator Commission Payable", {"policy_number": self.name}):
							com = frappe.new_doc("Operator Commission Payable")
							com.operator = self.operator
							com.policy = "B2B Policy Issue"
							com.status = "Unpaid"
							com.policy_number = self.name
							com.policy_date = self.date_of_issue
							com.commission_payable = commission 
							com.insert()
			
			else:
				customised_policy = frappe.get_doc("Customised Policy", self.policy_name)
				if customised_policy.policy_commission_type:
					if customised_policy.policy_commission_type == "Percentage":
						if customised_policy.commission_percentage:
							perc = customised_policy.commission_percentage

							#Calculate Commission
							amount = self.amount
							commission = (amount * perc)/100
							#Insert Operator Commission Receivable
							if commission:
								if not frappe.db.exists("Operator Commission Payable", {"policy_number": self.name}):
									com = frappe.new_doc("Operator Commission Payable")
									com.operator = self.operator
									com.policy = "B2B Policy Issue"
									com.status = "Unpaid"
									com.policy_number = self.name
									com.policy_date = self.date_of_issue
									com.commission_payable = commission 
									com.insert()

					elif customised_policy.policy_commission_type == "Amount":
						if customised_policy.commission_amount:
							#Calculate Commission
							commission = customised_policy.commission_amount
							#Insert Operator Commission Receivable

							if not frappe.db.exists("Operator Commission Payable", {"policy_number": self.name}):
								com = frappe.new_doc("Operator Commission Payable")
								com.operator = self.operator
								com.policy = "B2B Policy Issue"
								com.status = "Unpaid"
								com.policy_number = self.name
								com.policy_date = self.date_of_issue
								com.commission_payable = commission 
								com.insert()

	def before_update_after_submit(self):
		if self.policy_type == "Bulk Policy":
			if len(self.bulk_upload) == len(self.policy_list):
				self.pdf_added = "Completed"

	def validate_customer_details(self, customer, email, phone_number, date_of_birth):
		email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		mobile_format = r'\b[0-9]{12}$\b'
		min_age_limit = frappe.get_value("Customised Policy", self.policy_name, "min_age_limit")
		max_age_limit = frappe.get_value("Customised Policy", self.policy_name, "max_age_limit")
		today = dt.now().date()

		if email:
			if not fullmatch(email_format, email):
				frappe.throw(f"Email address of customer {customer} is invalid.")

		if phone_number:
			if not fullmatch(mobile_format, phone_number):
				frappe.throw(f"Contact number of customer {customer} is invalid. Make sure country code without '+' is mentioned.")
		
		if date_of_birth:
			if isinstance(date_of_birth, str):
				date_of_birth = dt.strptime(date_of_birth, "%Y-%m-%d").date()

			if min_age_limit and max_age_limit:
				
				age_of_customer = today.year - date_of_birth.year

				if not int(min_age_limit) <= age_of_customer <= int(max_age_limit):
					frappe.throw(f"Date of Birth of customer {customer} is invalid. Minimum age limit for this policy is {min_age_limit} and maximum age limit is {max_age_limit}.")
			else:
				if date_of_birth > today:
					frappe.throw(f"Date of Birth of customer {customer} is invalid.")
