# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BookingWebForm(Document):
	def after_insert(self):
		prod = self.operator_product
		book_date = self.booking_date
		time = self.time_of_day_of_activity
		doc = self.doctor_or_medical_practitioner_on_site
		ratio = self.manager_or_trainer_to_group_members_ratio
		activity_date = self.activity_date
		nature = self.nature_of_activity
		insurance = self.any_previous_insurance_ever_been_declined
		amount = self.total_amount
		booking = frappe.new_doc("Booking") 
		booking.operator_product = prod 
		booking.booking_date = book_date 
		booking.time_of_day_of_activity = time
		booking.doctor_or_medical_practitioner_on_site = doc 
		booking.manager_or_trainer_to_group_members_ratio = ratio 
		booking.activity_date = activity_date 
		booking.nature_of_activity = nature 
		booking.any_previous_insurance_ever_been_declined = insurance 
		booking.total_amount = amount 
		booking.submit()