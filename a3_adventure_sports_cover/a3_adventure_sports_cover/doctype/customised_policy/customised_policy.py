# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime
from warnings import filters
from frappe.model.document import Document
from frappe import get_all, get_doc, msgprint, new_doc, sendmail
import frappe


class CustomisedPolicy(Document):
	def on_cancel(self):
		plan_list = frappe.get_list("Item", filters={"parent_policy": self.name})
		for item in plan_list:
			it = frappe.get_doc("Item", item.name)
			print(it.disabled)
			it.disabled = 1
			it.save()
			# frappe.db.commit()
		
	
	def validate(self):
		if not self.policy_name:
			frappe.throw("Please enter Policy Name.")
			
		today = datetime.now()
		if datetime.strptime(self.plan_end_date, "%Y-%m-%d").date() <= today.date():
			frappe.throw("Plan End Date cannot be a past date or current date.")

		# Update policy premium in selected row
		if self.package_policy == 0:
			policy_master = get_doc("Policy Master", self.parent_policy)
			policy_master_list = []
			for mother_policy_plans in policy_master.insurance_plan_details:
				policy_master_list.append(mother_policy_plans.policy_benefits)
			
			if len(self.insurance_plan_details)>0:
				master_policy_list = []
				for policy_master_plan in self.insurance_plan_details:
					if policy_master_plan.policy_benefits not in policy_master_list:
						frappe.throw(f"Policy Benefit '{policy_master_plan.policy_benefits}' is not available in Mother Policy")
					
					# Check if Benefit Amount is less than or equal to Benefits amount of Mother Policy
					else:
						if policy_master_plan.policy_benefits in master_policy_list:
							frappe.throw(f"Policy Benefit '{policy_master_plan.policy_benefits}' already exists.")
						else:
							master_policy_list.append(policy_master_plan.policy_benefits)
							
						for mother_plan in policy_master.insurance_plan_details:
							if mother_plan.policy_benefits == policy_master_plan.policy_benefits:
								plan_list = [mother_plan.plan_1, mother_plan.plan_2, mother_plan.plan_3, mother_plan.plan_4, mother_plan.plan_5, mother_plan.plan_6, mother_plan.plan_7, mother_plan.plan_8, mother_plan.plan_9, mother_plan.plan_10]
								mother_plan_list = [policy_master_plan.plan_1, policy_master_plan.plan_2, policy_master_plan.plan_3, policy_master_plan.plan_4, policy_master_plan.plan_5, policy_master_plan.plan_6, policy_master_plan.plan_7, policy_master_plan.plan_8, policy_master_plan.plan_9, policy_master_plan.plan_10]
								for pl_list in range(10):
									if mother_plan_list[pl_list]:
										if str(plan_list[pl_list]) < str(mother_plan_list[pl_list]):
											frappe.throw(f"{policy_master_plan.policy_benefits} has higher amount in option than Mother Policy.")
			
			if self.max_age_limit:
				if policy_master.max_age_limit:
					if self.max_age_limit > policy_master.max_age_limit:
						frappe.throw("Maximum age limit should not more than Maximum age limit of Policy Master.")
			
			if self.min_age_limit:
				if policy_master.min_age_limit:
					if policy_master.min_age_limit > self.min_age_limit:
						frappe.throw("Minimum Age limit cannot be less than minimum age limit of Mother Policy.")

			if len(self.policy_premium)>0:
				for pol_prem in range(len(policy_master.policy_premium)):
					for prem in self.policy_premium:
						if prem.update_by:
							if prem.update_type == "Increase":
								if prem.update_amount_type == "Percentage":
									#Increase the premium amount in Percentage amount
									if prem.maximum_trip_duration == policy_master.policy_premium[pol_prem].maximum_trip_duration:
										prem.plan_1 = float(policy_master.policy_premium[pol_prem].plan_1) + (float(policy_master.policy_premium[pol_prem].plan_1)/100*float(prem.update_by))
										prem.plan_2 = float(policy_master.policy_premium[pol_prem].plan_2) + (float(policy_master.policy_premium[pol_prem].plan_2)/100*float(prem.update_by))
										prem.plan_3 = float(policy_master.policy_premium[pol_prem].plan_3) + (float(policy_master.policy_premium[pol_prem].plan_3)/100*float(prem.update_by))
										prem.plan_4 = float(policy_master.policy_premium[pol_prem].plan_4) + (float(policy_master.policy_premium[pol_prem].plan_4)/100*float(prem.update_by))
										prem.plan_5 = float(policy_master.policy_premium[pol_prem].plan_5) + (float(policy_master.policy_premium[pol_prem].plan_5)/100*float(prem.update_by))
										prem.plan_6 = float(policy_master.policy_premium[pol_prem].plan_6) + (float(policy_master.policy_premium[pol_prem].plan_6)/100*float(prem.update_by))
										prem.plan_7 = float(policy_master.policy_premium[pol_prem].plan_7) + (float(policy_master.policy_premium[pol_prem].plan_7)/100*float(prem.update_by))
										prem.plan_8 = float(policy_master.policy_premium[pol_prem].plan_8) + (float(policy_master.policy_premium[pol_prem].plan_8)/100*float(prem.update_by))
										prem.plan_9 = float(policy_master.policy_premium[pol_prem].plan_9) + (float(policy_master.policy_premium[pol_prem].plan_9)/100*float(prem.update_by))
										prem.plan_10 = float(policy_master.policy_premium[pol_prem].plan_10) + (float(policy_master.policy_premium[pol_prem].plan_10)/100*float(prem.update_by))
								elif prem.update_amount_type == "Amount":
									#Increase the premium amount in Amount
									if prem.maximum_trip_duration == policy_master.policy_premium[pol_prem].maximum_trip_duration:
										# Check if premium amount from mother policy is 0 or else add update amount
										if float(prem.plan_1) != 0.0: prem.plan_1 = float(policy_master.policy_premium[pol_prem].plan_1) + float(prem.update_by)
										if float(prem.plan_2) != 0.0: prem.plan_2 = float(policy_master.policy_premium[pol_prem].plan_2) + float(prem.update_by)
										if float(prem.plan_3) != 0.0: prem.plan_3 = float(policy_master.policy_premium[pol_prem].plan_3) + float(prem.update_by)
										if float(prem.plan_4) != 0.0: prem.plan_4 = float(policy_master.policy_premium[pol_prem].plan_4) + float(prem.update_by)
										if float(prem.plan_5) != 0.0: prem.plan_5 = float(policy_master.policy_premium[pol_prem].plan_5) + float(prem.update_by)
										if float(prem.plan_6) != 0.0: prem.plan_6 = float(policy_master.policy_premium[pol_prem].plan_6) + float(prem.update_by)
										if float(prem.plan_7) != 0.0: prem.plan_7 = float(policy_master.policy_premium[pol_prem].plan_7) + float(prem.update_by)
										if float(prem.plan_8) != 0.0: prem.plan_8 = float(policy_master.policy_premium[pol_prem].plan_8) + float(prem.update_by)
										if float(prem.plan_9) != 0.0: prem.plan_9 = float(policy_master.policy_premium[pol_prem].plan_9) + float(prem.update_by)
										if float(prem.plan_10) != 0.0: prem.plan_10 = float(policy_master.policy_premium[pol_prem].plan_10) + float(prem.update_by)
							if prem.update_type == "Decrease":
								# Decrease the amount in Percentage
								if prem.update_amount_type == "Percentage":
									if prem.maximum_trip_duration == policy_master.policy_premium[pol_prem].maximum_trip_duration:
										prem.plan_1 = float(policy_master.policy_premium[pol_prem].plan_1) - (float(policy_master.policy_premium[pol_prem].plan_1)/100*float(prem.update_by))
										prem.plan_2 = float(policy_master.policy_premium[pol_prem].plan_2) - (float(policy_master.policy_premium[pol_prem].plan_2)/100*float(prem.update_by))
										prem.plan_3 = float(policy_master.policy_premium[pol_prem].plan_3) - (float(policy_master.policy_premium[pol_prem].plan_3)/100*float(prem.update_by))
										prem.plan_4 = float(policy_master.policy_premium[pol_prem].plan_4) - (float(policy_master.policy_premium[pol_prem].plan_4)/100*float(prem.update_by))
										prem.plan_5 = float(policy_master.policy_premium[pol_prem].plan_5) - (float(policy_master.policy_premium[pol_prem].plan_5)/100*float(prem.update_by))
										prem.plan_6 = float(policy_master.policy_premium[pol_prem].plan_6) - (float(policy_master.policy_premium[pol_prem].plan_6)/100*float(prem.update_by))
										prem.plan_7 = float(policy_master.policy_premium[pol_prem].plan_7) - (float(policy_master.policy_premium[pol_prem].plan_7)/100*float(prem.update_by))
										prem.plan_8 = float(policy_master.policy_premium[pol_prem].plan_8) - (float(policy_master.policy_premium[pol_prem].plan_8)/100*float(prem.update_by))
										prem.plan_9 = float(policy_master.policy_premium[pol_prem].plan_9) - (float(policy_master.policy_premium[pol_prem].plan_9)/100*float(prem.update_by))
										prem.plan_10 = float(policy_master.policy_premium[pol_prem].plan_10) - (float(policy_master.policy_premium[pol_prem].plan_10)/100*float(prem.update_by))
								elif prem.update_amount_type == "Amount":
									# Decrease the amount in Amount
									if prem.maximum_trip_duration == policy_master.policy_premium[pol_prem].maximum_trip_duration:
										# Check if the premium amount is 0 or else minus update amount to it
										if float(prem.plan_1) != 0.0: prem.plan_1 = float(policy_master.policy_premium[pol_prem].plan_1) - float(prem.update_by)
										if float(prem.plan_2) != 0.0: prem.plan_2 = float(policy_master.policy_premium[pol_prem].plan_2) - float(prem.update_by)
										if float(prem.plan_3) != 0.0: prem.plan_3 = float(policy_master.policy_premium[pol_prem].plan_3) - float(prem.update_by)
										if float(prem.plan_4) != 0.0: prem.plan_4 = float(policy_master.policy_premium[pol_prem].plan_4) - float(prem.update_by)
										if float(prem.plan_5) != 0.0: prem.plan_5 = float(policy_master.policy_premium[pol_prem].plan_5) - float(prem.update_by)
										if float(prem.plan_6) != 0.0: prem.plan_6 = float(policy_master.policy_premium[pol_prem].plan_6) - float(prem.update_by)
										if float(prem.plan_7) != 0.0: prem.plan_7 = float(policy_master.policy_premium[pol_prem].plan_7) - float(prem.update_by)
										if float(prem.plan_8) != 0.0: prem.plan_8 = float(policy_master.policy_premium[pol_prem].plan_8) - float(prem.update_by)
										if float(prem.plan_9) != 0.0: prem.plan_9 = float(policy_master.policy_premium[pol_prem].plan_9) - float(prem.update_by)
										if float(prem.plan_10) != 0.0: prem.plan_10 = float(policy_master.policy_premium[pol_prem].plan_10) - float(prem.update_by)
							
			# Update Policy Premium in every row
			if self.update_type == "Increase":
				if self.update_amount_type == "Percentage":
					#Increase the premium amount in Percentage amount
					for premium in range(len(policy_master.policy_premium)):
						for prem in self.policy_premium:
							if not prem.update_by:
								if prem.maximum_trip_duration == policy_master.policy_premium[premium].maximum_trip_duration:
									prem.plan_1 = float(policy_master.policy_premium[premium].plan_1) + (float(policy_master.policy_premium[premium].plan_1)/100*float(self.update_amount))
									prem.plan_2 = float(policy_master.policy_premium[premium].plan_2) + (float(policy_master.policy_premium[premium].plan_2)/100*float(self.update_amount))
									prem.plan_3 = float(policy_master.policy_premium[premium].plan_3) + (float(policy_master.policy_premium[premium].plan_3)/100*float(self.update_amount))
									prem.plan_4 = float(policy_master.policy_premium[premium].plan_4) + (float(policy_master.policy_premium[premium].plan_4)/100*float(self.update_amount))
									prem.plan_5 = float(policy_master.policy_premium[premium].plan_5) + (float(policy_master.policy_premium[premium].plan_5)/100*float(self.update_amount))
									prem.plan_6 = float(policy_master.policy_premium[premium].plan_6) + (float(policy_master.policy_premium[premium].plan_6)/100*float(self.update_amount))
									prem.plan_7 = float(policy_master.policy_premium[premium].plan_7) + (float(policy_master.policy_premium[premium].plan_7)/100*float(self.update_amount))
									prem.plan_8 = float(policy_master.policy_premium[premium].plan_8) + (float(policy_master.policy_premium[premium].plan_8)/100*float(self.update_amount))
									prem.plan_9 = float(policy_master.policy_premium[premium].plan_9) + (float(policy_master.policy_premium[premium].plan_9)/100*float(self.update_amount))
									prem.plan_10 = float(policy_master.policy_premium[premium].plan_10) + (float(policy_master.policy_premium[premium].plan_10)/100*float(self.update_amount))
				elif self.update_amount_type == "Amount":
					#Increase the premium amount in Amount
					for premium in range(len(policy_master.policy_premium)):
						for prem in self.policy_premium:
							if not prem.update_by:
								if prem.maximum_trip_duration == policy_master.policy_premium[premium].maximum_trip_duration:
									# Check if premium amount from mother policy is 0 or else add update amount
									if float(prem.plan_1) != 0.0: prem.plan_1 = float(policy_master.policy_premium[premium].plan_1) + float(self.update_amount)
									if float(prem.plan_2) != 0.0: prem.plan_2 = float(policy_master.policy_premium[premium].plan_2) + float(self.update_amount)
									if float(prem.plan_3) != 0.0: prem.plan_3 = float(policy_master.policy_premium[premium].plan_3) + float(self.update_amount)
									if float(prem.plan_4) != 0.0: prem.plan_4 = float(policy_master.policy_premium[premium].plan_4) + float(self.update_amount)
									if float(prem.plan_5) != 0.0: prem.plan_5 = float(policy_master.policy_premium[premium].plan_5) + float(self.update_amount)
									if float(prem.plan_6) != 0.0: prem.plan_6 = float(policy_master.policy_premium[premium].plan_6) + float(self.update_amount)
									if float(prem.plan_7) != 0.0: prem.plan_7 = float(policy_master.policy_premium[premium].plan_7) + float(self.update_amount)
									if float(prem.plan_8) != 0.0: prem.plan_8 = float(policy_master.policy_premium[premium].plan_8) + float(self.update_amount)
									if float(prem.plan_9) != 0.0: prem.plan_9 = float(policy_master.policy_premium[premium].plan_9) + float(self.update_amount)
									if float(prem.plan_10) != 0.0: prem.plan_10 = float(policy_master.policy_premium[premium].plan_10) + float(self.update_amount)
			elif self.update_type == "Decrease":
				if self.update_amount_type == "Percentage":
					# Decrease the amount in Percentage
					for premium in range(len(policy_master.policy_premium)):
						for prem in self.policy_premium:
							if not prem.update_by:
								if prem.maximum_trip_duration == policy_master.policy_premium[premium].maximum_trip_duration:
									prem.plan_1 = float(policy_master.policy_premium[premium].plan_1) - (float(policy_master.policy_premium[premium].plan_1)/100*float(self.update_amount))
									prem.plan_2 = float(policy_master.policy_premium[premium].plan_2) - (float(policy_master.policy_premium[premium].plan_2)/100*float(self.update_amount))
									prem.plan_3 = float(policy_master.policy_premium[premium].plan_3) - (float(policy_master.policy_premium[premium].plan_3)/100*float(self.update_amount))
									prem.plan_4 = float(policy_master.policy_premium[premium].plan_4) - (float(policy_master.policy_premium[premium].plan_4)/100*float(self.update_amount))
									prem.plan_5 = float(policy_master.policy_premium[premium].plan_5) - (float(policy_master.policy_premium[premium].plan_5)/100*float(self.update_amount))
									prem.plan_6 = float(policy_master.policy_premium[premium].plan_6) - (float(policy_master.policy_premium[premium].plan_6)/100*float(self.update_amount))
									prem.plan_7 = float(policy_master.policy_premium[premium].plan_7) - (float(policy_master.policy_premium[premium].plan_7)/100*float(self.update_amount))
									prem.plan_8 = float(policy_master.policy_premium[premium].plan_8) - (float(policy_master.policy_premium[premium].plan_8)/100*float(self.update_amount))
									prem.plan_9 = float(policy_master.policy_premium[premium].plan_9) - (float(policy_master.policy_premium[premium].plan_9)/100*float(self.update_amount))
									prem.plan_10 = float(policy_master.policy_premium[premium].plan_10) - (float(policy_master.policy_premium[premium].plan_10)/100*float(self.update_amount))
				elif self.update_amount_type == "Amount":
					# Decrease the amount in Amount
					for premium in range(len(policy_master.policy_premium)):
						for prem in self.policy_premium:
							if not prem.update_by:
								if prem.maximum_trip_duration == policy_master.policy_premium[premium].maximum_trip_duration:
									# Check if the premium amount is 0 or else minus update amount to it
									if float(prem.plan_1) != 0.0: prem.plan_1 = float(policy_master.policy_premium[premium].plan_1) - float(self.update_amount)
									if float(prem.plan_2) != 0.0: prem.plan_2 = float(policy_master.policy_premium[premium].plan_2) - float(self.update_amount)
									if float(prem.plan_3) != 0.0: prem.plan_3 = float(policy_master.policy_premium[premium].plan_3) - float(self.update_amount)
									if float(prem.plan_4) != 0.0: prem.plan_4 = float(policy_master.policy_premium[premium].plan_4) - float(self.update_amount)
									if float(prem.plan_5) != 0.0: prem.plan_5 = float(policy_master.policy_premium[premium].plan_5) - float(self.update_amount)
									if float(prem.plan_6) != 0.0: prem.plan_6 = float(policy_master.policy_premium[premium].plan_6) - float(self.update_amount)
									if float(prem.plan_7) != 0.0: prem.plan_7 = float(policy_master.policy_premium[premium].plan_7) - float(self.update_amount)
									if float(prem.plan_8) != 0.0: prem.plan_8 = float(policy_master.policy_premium[premium].plan_8) - float(self.update_amount)
									if float(prem.plan_9) != 0.0: prem.plan_9 = float(policy_master.policy_premium[premium].plan_9) - float(self.update_amount)
									if float(prem.plan_10) != 0.0: prem.plan_10 = float(policy_master.policy_premium[premium].plan_10) - float(self.update_amount)
		else:
			if len(self.parent_list)>0:
				primary = False
				age_val = 0
				for parent in self.parent_policy:
					master_policy = get_doc("Policy Master", parent.parent_policy)
					if master_policy.max_age_limit and master_policy.min_age_limit:
						age_cal = float(master_policy.max_age_limit) - float(master_policy.min_age_limit)
						if age_cal>age_val:
							age_val = age_cal
							self.min_age_limit = master_policy.min_age_limit
							self.max_age_limit = master_policy.max_age_limit
					
					if parent.primary_policy == 1:
						if not primary:
							primary = True
							self.scope_of_policy = master_policy.scope_of_policy
							self.type_of_policy = master_policy.type_of_policy
						else:
							frappe.throw("You can only select one primary Mother Policy.")
				
				if not primary:
					frappe.throw("Please select one primary Mother Policy")



	def on_submit(self):
		if self.operator_status == "Pending Approval":
			frappe.throw("This Customised Policy is pending to be approved.")
		elif self.operator_status == "Approved":
			for prem in range(len(self.policy_premium)):
				plans = [self.policy_premium[prem].plan_1, self.policy_premium[prem].plan_2, self.policy_premium[prem].plan_3, self.policy_premium[prem].plan_4]
				for index in range(4):

					if plans[index] != 0:
						name = f"{self.name} - {self.policy_premium[prem].maximum_trip_duration} Days - Plan {index+1}"
						frappe.db.sql("""
								INSERT INTO `tabItem` (name, item_name, item_code, standard_rate, stock_uom, item_group,master_policy,period_of_issuance,parent_policy,max_age,min_age)
								VALUES
									(%(name)s, %(item_name)s, %(item_code)s, %(standard_rate)s, %(stock_uom)s, %(item_group)s, %(master_policy)s, %(period_of_issuance)s, %(parent_policy)s, %(max_age)s,%(min_age)s);
							""",
							dict(
								name = name,
								item_name = name,
								item_code = name,
								period_of_issuance = self.policy_premium[prem].maximum_trip_duration,
								standard_rate = plans[index],
								stock_uom = "Nos",
								item_group = "All Item Groups",
								master_policy = self.parent_policy,
								parent_policy = self.name,
								max_age = self.max_age_limit,
								min_age = self.min_age_limit
							)
						)

						price_list = get_doc("Price List", {"currency": self.premium_currency})
						item_price = new_doc('Item Price')
						item_price.item_code = f"{self.name} - {self.policy_premium[prem].maximum_trip_duration} Days - Plan {index+1}"
						item_price.uom = 'Nos'
						item_price.selling = True
						item_price.price_list = price_list.name
						item_price.price_list_rate = plans[index]
						item_price.currency = self.premium_currency
						item_price.save()
						frappe.db.commit()

						item_benefits = get_doc("Item", name)
						for insurance_plan_detail in self.insurance_plan_details:
							plan_list = [insurance_plan_detail.plan_1, insurance_plan_detail.plan_2, insurance_plan_detail.plan_3, insurance_plan_detail.plan_4]
							item_benefits.append("benefit_details", {
								"benefit": insurance_plan_detail.policy_benefits,
								"amount": plan_list[index],
								"deductible": insurance_plan_detail.deductible
							})
						item_benefits.save()
			msgprint("Item(s) created!")
	
	def after_insert(self):
		if self.package_policy == 1:
			if len(self.parent_list)>0:
				self.insurance_plan_details.clear()
				self.policy_premium.clear()
				self.activity_list.clear()
				
				for parent in self.parent_list:
					parent.index = 1

					master_policy = get_doc("Policy Master", parent.parent_policy)
					self.fetch_data(master_policy)
				self.save()
				
	def before_insert(self):
		if self.operator_status != "Pending Approval":
			self.operator_status = "Pending Approval"

	def validate(self):
		if self.package_policy == 1:
			index = 1
			parent_policy_list = set()
			for plan in self.insurance_plan_details:
				parent_policy_list.add(plan.parent_policy)
			for parent in self.parent_list:
				if parent.index:
					if parent.index > index:
						index= parent.index
				else:
					parent.index = index
					master_policy = get_doc("Policy Master", parent.parent_policy)
					self.fetch_data(master_policy)
					
	
	def fetch_data(self, master_policy):
		for plan in  master_policy.insurance_plan_details:
			self.append("insurance_plan_details", {
				"policy_benefits": plan.policy_benefits,
				"plan_1": plan.plan_1,
				"plan_2": plan.plan_2,
				"plan_3": plan.plan_3,
				"plan_4": plan.plan_4,
				"plan_5": plan.plan_5,
				"plan_6": plan.plan_6,
				"plan_7": plan.plan_7,
				"plan_8": plan.plan_8,
				"plan_9": plan.plan_9,
				"plan_10": plan.plan_10,
				"deductible": plan.deductible,
				"parent_policy": master_policy.name
			})
		
		for premium in master_policy.policy_premium:
			self.append("policy_premium", {
				"maximum_trip_duration": premium.maximum_trip_duration,
				"plan_1": premium.plan_1,
				"plan_2": premium.plan_2,
				"plan_3": premium.plan_3,
				"plan_4": premium.plan_4,
				"plan_5": premium.plan_5,
				"plan_6": premium.plan_6,
				"plan_7": premium.plan_7,
				"plan_8": premium.plan_8,
				"plan_9": premium.plan_9,
				"plan_10": premium.plan_10,
				"parent_policy": master_policy.name
			})
		
		for activity in master_policy.activity_list:
			self.append("activity_list", {
				"activity_name": activity.activity_name,
				"level": activity.level,
				"mother_policy_level": activity.mother_policy_level,
				"category": activity.category,
				"parent_policy": master_policy.name
			})
