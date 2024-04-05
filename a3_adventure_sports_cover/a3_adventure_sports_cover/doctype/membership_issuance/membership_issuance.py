# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime, timedelta
from frappe.model.document import Document
import frappe

class MembershipIssuance(Document):
	# def before_insert(self):
	# 	#Naming Series
	# 	scope_id = ""
	# 	provider_id = ""

	# 	if self.plan:
	# 		pol = frappe.get_doc("Item", self.plan)
	# 		if pol.master_policy:
	# 			membership = frappe.get_doc("Annual Membership",pol.master_policy)
	# 			if membership.scope_of_policy:
	# 				scope = membership.scope_of_policy
	# 				if scope == "International":
	# 					scope_id = "I"
	# 				elif scope == "Domestic":
	# 					scope_id = "D"
	# 			if membership.policy_provider:
	# 				provider = membership.policy_provider
	# 				provider_id = provider[0]

					
	# 	today = datetime.today()
	# 	policy_list = frappe.get_list("List of Policy")
		
	# 	if len(policy_list) == 0:
	# 		series_no = 0
	# 	else:
	# 		last_doc = frappe.get_last_doc("List of Policy")
	# 		series_no = int(last_doc.series_number)+1

	# 	if scope_id!="" and provider:
	# 		policy_number = f"ASC360-{scope_id}{provider_id}-{today.month}-{today.year}-AM{'{:05d}'.format(series_no)}"
	# 	else:
	# 		policy_number = f"ASC360-MDBK-{today.month}-{today.year}-AM{'{:05d}'.format(series_no)}"

	# 	self.policy_number = policy_number

	def after_insert(self):
		# create a payment entry for the amount received from the customer
		pay = frappe.new_doc("Payment Entry")
		pay.party_type = "Customer"
		pay.party = self.customer
		pay.party_name = self.customer
		pay.paid_amount = self.premium
		pay.received_amount = self.premium
		pay.source_exchange_rate = 1.0
		pay.target_exchange_rate = 1.0
		pay.mode_of_payment = self.mode_of_payment
		pay.paid_to = self.account_paid_to
		if self.reference_no:
			pay.reference_no = self.reference_no
		if self.reference_date:
			pay.reference_date = self.reference_date
		if self.payment_collected_by:
			pay.payment_collected_by = self.payment_collected_by
		pay.save()
		pay.submit()

		# adding this policy to the list of policy
		# policy_list = frappe.get_list("List of Policy")
		# if len(policy_list)==0:
		# 	series_no = 0
		# else:
		# 	last_doc = frappe.get_last_doc("List of Policy")
		# 	series_no = int(last_doc.series_number)+1
		# list_of_policy = frappe.new_doc("List of Policy")
		# list_of_policy.document = "Membership Issuance"
		# list_of_policy.policy = self.policy_number
		# list_of_policy.start_date = self.start_date
		# list_of_policy.end_date = self.end_date
		# list_of_policy.series_number = series_no
		# list_of_policy.customer = self.customer
		# list_of_policy.date_of_birth = self.date_of_birth
		# list_of_policy.amount = self.premium
		# list_of_policy.policy_provider = self.policy_provider
		# list_of_policy.date_of_issue = self.date_of_issue
		# list_of_policy.insert()

	def before_update_after_submit(self):
		# Get current fiscal year start date and end date
		sdate = self.start_date
		edate = self.end_date

		if isinstance(sdate, str):
			sdate = datetime.strptime(sdate, "%Y-%m-%d").date()

		if isinstance(edate, str):
			edate = datetime.strptime(edate, "%Y-%m-%d").date()
	
		date_modified = sdate
		date_list = [sdate]

		# get all dates between two start date and end date
		while date_modified<edate:
			date_modified+=timedelta(days=1)
			date_list.append(date_modified)
		
		# check if total amount of activity is less than or equal to amount paid by the customer
		total_activity_amount = 0
		for activity in self.activities_list:
			total_activity_amount += activity.amount

			activity_date = activity.activity_date

			if isinstance(activity_date, str):
				activity_date = datetime.strptime(activity_date, "%Y-%m-%d").date()

			# check if activity date is in between start date and end date
			if activity_date not in date_list:
				frappe.throw(f"Activity '{activity.activity}' is not done during the currect membership. Please enter valid Activity Date.")
		
		if self.premium <  total_activity_amount:
			frappe.throw("You don't have enough credit to add more activities.")

	def validate(self):
		start_date = self.start_date
		end_date = self.end_date

		# check if start_date is string and change it to datetime data
		if isinstance(start_date, str):
			start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
		
		# check if end_date is string and change it to datetime data
		if isinstance(end_date, str):
			end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		
		# check if start_date is not a past date
		if start_date:
			today = datetime.today().date()
			if start_date < today:
				frappe.throw("Start Date cannot be a past date. Please check.")
		
		# check if end_date is not a past date
		if end_date:
			if start_date > end_date:
				frappe.throw("End Date cannot be a past Start Date. Please check.")

		#Create customer address if not already exists
		if self.address_line_1:
			get_address = frappe.db.exists("Address", {"address_title": self.customer})
			if get_address == None:
				add = frappe.new_doc("Address")
				add.address_title = self.customer
				add.address_type = "Billing"
				add.address_line1 = self.address_line_1
				add.address_line2 = self.address_line_2
				add.city = self.city
				add.state = self.state
				add.country = self.country
				add.pincode = self.pin_code

				add.append("links", {
					"link_doctype" : "Customer",
					"link_name" : self.customer
				})
				add.insert()

	def before_submit(self):
		self.balance_available = self.premium


