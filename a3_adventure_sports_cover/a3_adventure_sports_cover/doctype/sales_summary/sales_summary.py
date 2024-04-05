# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class SalesSummary(Document):
	def validate(self):
		grand_total = 0 
		if self.invoices:
			for row in self.invoices:
				if row.total:
					grand_total = grand_total+float(row.total)
			self.grand_total = grand_total

		for row in self.invoices:
			if row.date:
				date_str = str(row.date)
				date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
				month = str(date.month) 
				month_str = datetime.datetime.strptime(month, "%m")
				month_name = month_str.strftime("%b")
				row.month = month_name 
				row.day = date.day
				row.year = date.year

		unique_items = []
		for row in self.invoices:
			item = row.policy
			if not item in unique_items:
				unique_items.append(item)
			item_total = 0

		self.item_total.clear()
		for x in unique_items:
			price = 0
			for items in self.invoices:
				if items.policy == x:
					price = price + items.total 
			self.append("item_total",
			{
				"item": x,
				"total": price 
			})
			
			

		
