# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BookingSummary(Document):
	def validate(self):
		total = 0
		if self.bookings:
			for row in self.bookings:
				total = total+row.amount
		
		self.grand_total = total 

		unique_items = []
		for row in self.bookings:
			item = row.operator_product
			if not item in unique_items:
				unique_items.append(item)

		self.product_wise_total.clear()
		price = 0
		for x in unique_items:
			for items in self.bookings:
				if items.operator_product == x:
					price = price + items.amount 
					self.append("product_wise_total",
					{
						"product": x,
						"total": price 
					})


