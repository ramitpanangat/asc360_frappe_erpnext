
from frappe.model.document import Document
from frappe.utils import pdf, file_manager
from frappe.core.doctype.file.file import create_new_folder
from datetime import datetime as dt, timedelta
from a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2c_policy_issue.events import attach_pdf
import frappe
import datetime
import requests

class B2CPolicyIssue(Document):
	def before_insert(self):
		#If policy is of Single Type
		#Naming Series
		if self.policy_type == "Single Policy":
			if self.endorse == 0:
				scope_id = ""
				type_id = ""
				provider_id = ""

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
							
				today = dt.today()
				policy_list = frappe.get_list("List of Policy")
				if len(policy_list)==0:
					series_no = 0
				else:
					last_doc = frappe.get_last_doc("List of Policy")
					series_no = int(last_doc.series_number)+1
				if scope_id != "" and type_id != "" and provider_id != "":
					policy_number = f"ASC360-{scope_id}{type_id}{provider_id}-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"
				else:
					policy_number = f"ASC360-MDBK-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"

				self.policy_number = policy_number
			else:
				self.policy_number = f"{self.original_policy} - {self.endorsement_count}"

			#Fetch Payment Details
			if self.endorse == 0:
				if self.invoice_and_payment:
					if self.payment_id:
						paym = frappe.get_doc("Payment Entry",self.payment_id)
						if paym.payment_collected_by:
							self.payment_collected_by = paym.payment_collected_by
						if paym.mode_of_payment:
							self.mode_of_payment = paym.mode_of_payment
						if paym.paid_to:
							self.account_paid_to = paym.paid_to
						if paym.paid_amount:
							self.paid_amount = paym.paid_amount
						if paym.reference_no:
							self.reference_no = paym.reference_no
						if paym.reference_date:
							self.reference_date = paym.reference_date 
			if self.add_new_customer == 0:
				if self.customer_name:
					self.customer = self.customer_name 
		
		#If policy is of Bulk Type
		elif self.policy_type == "Bulk Policy":
			#Naming Series
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
		if self.policy_status != "In Process":
			self.policy_status = "In Process"

		#Fetching data
		item = frappe.get_doc("Item", self.policy)
		# if self.start_date:
		# 	self.period_of_issuance = item.period_of_issuance

		# if self.policy:
		# 	self.amount = item.standard_rate

		self.policy_provider = frappe.get_value("Policy Master", item.master_policy, "policy_provider")

		self.save()

		
		#Adding policy List Of Policy Doctype
		if self.policy_type == "Bulk Policy":
			bulk_series_list = frappe.get_list("Bulk Policy Series Number")
			if len(bulk_series_list) == 0:
				series_no = 0
			else:
				last_doc = frappe.get_last_doc("Bulk Policy Series Number")
				series_no = int(last_doc.series_number)+1
			bulk_series = frappe.new_doc("Bulk Policy Series Number")
			bulk_series.series_number = series_no
			bulk_series.insert()

		elif self.policy_type == "Single Policy":
			policy_list = frappe.get_list("List of Policy")
			if len(policy_list)==0:
				series_no = 0
			else:
				last_doc = frappe.get_last_doc("List of Policy")
				series_no = int(last_doc.series_number)+1
			list_of_policy = frappe.new_doc("List of Policy")
			list_of_policy.document = "B2C Policy Issue"
			list_of_policy.policy = self.policy_number
			list_of_policy.series_number = series_no
			list_of_policy.customer = self.customer_name
			list_of_policy.start_date = self.start_date
			list_of_policy.end_date = self.end_date
			list_of_policy.date_of_birth = self.date_of_birth
			list_of_policy.period_of_issuance = self.period_of_issuance 
			list_of_policy.amount = self.amount
			list_of_policy.policy_provider = self.policy_provider
			list_of_policy.date_of_issue = self.date_of_issuance
			list_of_policy.insert()
		
		#Validate Paid Amount against Premium Amount
		# if self.amount < self.paid_amount:
		#     frappe.msgprint("Policy Premium Greater than Paid Amount!")

	def on_submit(self):
		# #Validate Start Date !< Today
		today = datetime.datetime.today().date()
		start = self.start_date
		if isinstance(start, str):
			start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
		r = (start - today)
		days = r.days + 1   #to rectify today-today = -1
		if self.admin_approved == 0:
			if days < 0:
				frappe.throw("Start Date Has to be Greater than or Equal to Date of Issue!")

		# #Validate End Date !< Start Date
		end = self.end_date
		if isinstance(end, str):
			end = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()
		if end < start:
			frappe.throw("End Date cannot be Before Start Date!")

		#Validate Age Limit
		if self.policy_type == "Single Policy":
			today = datetime.datetime.today().year
			dob = datetime.datetime.strptime(str(self.date_of_birth), "%Y-%m-%d").year
			age = float(today - dob)
			item = frappe.get_doc("Item",self.policy)
			if item.min_age:
				min = float(item.min_age)
				if age <= min:
					frappe.throw("Customer Age is Less Than Minimum Age Limit!!")
			if item.max_age:
				max = float(item.max_age)
				if age >= max:
					frappe.throw("Customer Age is Greater Than Maximum Age Limit!!")

			#Create Customer Invoice 
			if self.endorse == 0:
				if self.invoice_and_payment == 0:   
					self.create_invoice()
			self.check_membership()
			# attach_pdf(self)

		if self.policy_type == "Bulk Policy":
			queue_doc = frappe.get_single("B2C Policy Queue")
			index = 1
			for cust in self.customer_bulk:
				if cust.address_line_1:
					if not cust.city:
						frappe.throw(f"Row number {index} requires City field to add Address.")
					if not cust.country:
						frappe.throw(f"Row number {index} requires Country field to add Address.")

				queue_doc.append("policy_list", {
					"priority_ranking": queue_doc.no_of_batches + 1,
					"main_policy": self.name,
					"customer_name": str(cust.customer).strip(),
					"gender": str(cust.gender).strip(),
					"date_of_birth": cust.date_of_birth,
					"email_id": str(cust.email).strip(),
					"contact": str(cust.phone_number).strip(),
					"address": cust.address_line_1,
					"address_line_2": cust.address_line_2,
					"city_town": cust.city,
					"state": cust.state,
					"country": cust.country,
					"pincode": cust.pin_code,
					"nationality": cust.nationality,
					"event": cust.event,
					"pan_number": cust.pan_number,
					"aadhar_number": cust.aadhar_card,
					"passport_number": cust.passport_number,
					"nominee_name": cust.nomine_name,
					"nominee_contact": cust.nominee_contact,
					"nominee_relationship": cust.nominee_relationship,
					"admin_approved": self.admin_approved
				})
				index += 1
			queue_doc.no_of_batches = queue_doc.no_of_batches + 1
			queue_doc.save()

	def validate(self):
		#Calculate Period of Issuance = End Date - Start Date
		if self.start_date and self.end_date:
			start = self.start_date
			end = self.end_date
			if isinstance(start, str):
				start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
			if isinstance(end, str):
				end = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()
			p = end - start 
			self.period_of_issuance = p.days + 1

		if self.date_of_birth:
			date_of_issue = datetime.datetime.strptime(self.date_of_issuance, "%Y-%m-%d").date()
			date_of_birth = datetime.datetime.strptime(str(self.date_of_birth), "%Y-%m-%d").date()
			diff = date_of_issue - date_of_birth
			if date_of_issue < date_of_birth or diff.days < 366:
				frappe.throw("Invalid Date of Birth")


		if self.policy_type == "Bulk Policy":
			
			if self.exchange_rate:
				if len(self.customer_bulk)>0:
					converted_amount = self.amount * self.exchange_rate
					self.premium_in_inr = converted_amount * len(self.customer_bulk)
				else:
					self.premium_in_inr = 0

		if self.policy_type == "Single Policy":
			if self.exchange_rate:
				converted_amount = self.amount * self.exchange_rate
				self.premium_in_inr = converted_amount 
			
		if self.policy:
			item_price = frappe.get_doc("Item Price",{"item_code":self.policy})
			if item_price.currency:
				self.premiun_currency = item_price.currency
		
	def create_invoice(self):
		today = datetime.datetime.now().date()
		invoice = frappe.new_doc("Sales Invoice")
		invoice.customer = self.customer_name
		invoice.due_date = self.date_of_issuance
		invoice.policy_number = self.name
		invoice.status="Paid"
		invoice.b2c = 1
		invoice.append(
			"items",
			{
				"item_code": self.policy,
				"rate": self.amount
			},
		)
		invoice.set_missing_values()
		invoice.insert()
		invoice.submit()
		self.invoice_number = invoice.name

		if self.paid_amount and self.customer_name and self.invoice_and_payment == 0:
			pay = frappe.new_doc("Payment Entry")
			pay.party_type = "Customer"
			pay.party = self.customer_name
			pay.party_name = self.customer_name
			pay.paid_amount = self.paid_amount
			pay.received_amount = self.paid_amount
			pay.target_exchange_rate = self.exchange_rate
			pay.mode_of_payment = self.mode_of_payment
			pay.policy_number = self.name
			pay.paid_to = self.account_paid_to
			if self.reference_no:
				pay.reference_no = self.reference_no
			if self.reference_date:
				pay.reference_date = self.reference_date
			if self.payment_collected_by:
				pay.payment_collected_by = self.payment_collected_by
			pay.append("references", {
				"reference_doctype": "Sales Invoice",
				"reference_name" : invoice.name,
				"total_amount": self.premium_in_inr,
				"due_date": invoice.due_date,
			})
			self.payment_id = pay.name
			self.db_update()
			pay.insert()
			pay.submit()

			invoice.status = "Paid"
			invoice.db_update()
		frappe.msgprint("Sales Invoice generated & Submitted successfully")
	
	def check_membership(self):
		if self.has_membership == "Yes":
			membership_issue = frappe.get_doc("Membership Issuance", self.membership_id)
			membership_issue.append("activities_list", {
				"type_of_policy": self.doctype,
				"policy_number": self.name,
				"amount": self.premium_in_inr,
				"activity_date": self.date_of_issuance
			})
			balance = membership_issue.balance_available
			for activity in membership_issue.activities_list:
				balance -= activity.amount
			membership_issue.balance_available = balance
			membership_issue.save()
			membership_issue.db_update()
	
	def before_update_after_submit(self):
		if self.policy_type == "Bulk Policy":
			if len(self.customer_bulk) == len(self.policy_generated_list):
				self.policy_status = "Completed"
	
	def before_submit(self):
		if self.add_new_customer == 1:
			if not frappe.db.exists("Customer", {"customer_name":self.customer, "email_id":self.email_id, "mobile_no":self.phone_number}):
				date_of_birth = self.date_of_birth
				if isinstance(date_of_birth, str):
					date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
					
				customer = frappe.new_doc("Customer")
				customer.customer_name = self.customer
				customer.customer_type = "Individual"
				customer.territory = "India"
				customer.customer_group = "Individual"
				customer.gender = self.gender
				customer.date_of_birth = date_of_birth
				customer.customer_name = self.customer

				for proofs in self.id_proof_documents:
					if proofs.document_type == "Passport":
						customer.passport_number = proofs.documnet_number
					if proofs.document_type == "Aadhaar Card":
						customer.aadhaar_card = proofs.documnet_number
					if proofs.document_type == "PAN Card":
						customer.pan = proofs.documnet_number
				customer.insert()

				contact = frappe.new_doc("Contact")
				print(self.customer)
				contact.first_name = self.customer
				contact.gender = self.gender
				contact.append("email_ids", {
					"email_id": self.email_id,
					"is_primary": 1
				})
				contact.append("phone_nos", {
					"phone": self.phone_number,
					"is_primary_phone": 1,
					"is_primary_mobile_no": 1
				})
				contact.append("links", {
					"link_doctype": "Customer",
					"link_name": customer.name,
					"link_title": customer.name
				})
				

				address = frappe.new_doc("Address")
				address.address_title = customer.name
				address.address_line1 = self.address_line_1
				address.address_line2 = self.address_line_2
				address.city = self.citytown
				address.state = self.state_ut
				address.country = self.country
				address.pincode = self.pin_code
				address.email_id = self.email_id
				address.phone = self.phone_number
				address.email_id = self.email_id
				address.append("links", {
					"link_doctype": "Customer",
					"link_name": customer.name,
					"link_title": customer.name
				})

				contact.insert()
				address.insert()
				customer.customer_primary_contact = contact.name
				customer.customer_primary_address = address.name
				
				customer.save()
				
				self.customer_name = customer.name


	def on_cancel(self):
		if self.policy_type == "Single Policy":
			if frappe.db.exists("List of Policy", {"policy": self.name}):
				lop = frappe.get_doc("List of Policy", {"policy": self.name})
				lop.policy_status = "Cancelled"
				lop.save()
			
			if frappe.db.exists("Sales Invoice", {"policy_number": self.name}):
				invoice = frappe.get_doc("Sales Invoice", {"policy_number": self.name})
				invoice.cancel()
			
			if frappe.db.exists("Payment Entry", self.payment_id):
				payment = frappe.get_doc("Payment Entry", self.payment_id)
				payment.cancel()

			if self.batch_id:
				bulk_doc = frappe.get_doc("B2C Policy Issue", self.batch_id)
				for policy in bulk_doc.policy_generated_list:
					if policy.policy_number == self.name:
						bulk_doc.policy_generated_list.remove(policy)
				bulk_doc.append("cancelled_policy",{
					"policy_number": self.name,
					"customer": self.customer_name,
					"cancelled_by": frappe.session.user,
					"cancelled_on": dt.now()
				})
				bulk_doc.save()
				bulk_doc.db_update()
		if self.policy_type == "Bulk Policy":
			for policy in self.policy_generated_list:
				policy_doc = frappe.get_doc("B2C Policy Issue", policy.policy_number)
				policy_doc.cancel()
		
					
