# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

class AnnualMembership(Document):
	def on_submit(self):
		for prem in range(len(self.policy_premium)):
			plans = [self.policy_premium[prem].plan_1, self.policy_premium[prem].plan_2, self.policy_premium[prem].plan_3, self.policy_premium[prem].plan_4]
			for index in range(4):

				if plans[index] != 0:
					name = f"{self.name} - {self.policy_premium[prem].maximum_trip_duration} Days - Plan {index+1}"
					item = frappe.new_doc("Item")
					item.name = name
					item.item_code = name
					item.period_of_issuance = self.policy_premium[prem].maximum_trip_duration
					item.standard_rate = plans[index]
					item.stock_uom = "Nos"
					item.item_group = "Annual Membership"
					item.membership_id = self.name
					item.insert()
