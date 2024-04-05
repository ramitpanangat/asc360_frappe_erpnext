# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

# import frappe
from frappe import get_doc
import frappe
from frappe.model.document import Document
from numpy import append

class PolicyMaster(Document):
	def on_update_after_submit(self):
		# If Policy Master is made inactive it will turn Customised Policy inactive and vice a versa
		if self.status == "Inactive":
			customised_policy_list = frappe.get_list("Customised Policy")
			for custome_policy in customised_policy_list:
				policy = get_doc("Customised Policy", custome_policy.name)
				if policy.parent_policy == self.name:
					policy.status = "Inactive"
					policy.db_update()

					plan_list = frappe.get_list("Item", filters={"parent_policy": policy.name})
					for item in plan_list:
						it = frappe.get_doc("Item", item.name)
						it.disabled = 1
						it.save()
		else:
			customised_policy_list = frappe.get_list("Customised Policy")
			for custome_policy in customised_policy_list:
				policy = get_doc("Customised Policy", custome_policy.name)
				if policy.parent_policy == self.name:
					policy.status = "Active"
					policy.db_update()

					plan_list = frappe.get_list("Item", filters={"parent_policy": policy.name})
					for item in plan_list:
						it = frappe.get_doc("Item", item.name)
						it.disabled = 0
						it.save()


	def validate(self):
		if not self.policy_name:
			frappe.throw("Please enter Policy Name.")
		
		# Update policy premium in selected row
		if self.package_policy == 0:
			# Check age limit with Mother Policy
			mother_policy = get_doc("Mother Policy", self.parent_policy)
			if self.max_age_limit:
				if mother_policy.max_age_limit:
					if mother_policy.max_age_limit < self.max_age_limit:
						frappe.throw("Maximum Age limit cannot be higher than maximum age limit of Mother Policy.")
			
			if self.min_age_limit:
				if mother_policy.min_age_limit:
					if mother_policy.min_age_limit > self.min_age_limit:
						frappe.throw("Minimum Age limit cannot be less than minimum age limit of Mother Policy.")
			self.increase_decrease_value(mother_policy)

			# Check if all plans are from mother policy and none is new from mother policy
			mother_policy_plan_list = []
			for mother_policy_plans in mother_policy.insurance_plan_details:
				mother_policy_plan_list.append(mother_policy_plans.policy_benefits)
			
			if len(self.insurance_plan_details)>0:
				policy_master_list = []

				for policy_master_plan in self.insurance_plan_details:
					if policy_master_plan.policy_benefits not in mother_policy_plan_list:
						frappe.throw(f"Policy Benefit '{policy_master_plan.policy_benefits}' is not available in Mother Policy")
					else:
						if policy_master_plan.policy_benefits in policy_master_list:
							frappe.throw(f"Policy Benefit '{policy_master_plan.policy_benefits}' already exits.")
						else:
							policy_master_list.append(policy_master_plan.policy_benefits)

						# Check if Benefit Amount is less than or equal to Benefits amount of Mother Policy
						for mother_plan in mother_policy.insurance_plan_details:
							if mother_plan.policy_benefits == policy_master_plan.policy_benefits:
								plan_list = [mother_plan.plan_1, mother_plan.plan_2, mother_plan.plan_3, mother_plan.plan_4, mother_plan.plan_5, mother_plan.plan_6, mother_plan.plan_7, mother_plan.plan_8, mother_plan.plan_9, mother_plan.plan_10]
								mother_plan_list = [policy_master_plan.plan_1, policy_master_plan.plan_2, policy_master_plan.plan_3, policy_master_plan.plan_4, policy_master_plan.plan_5, policy_master_plan.plan_6, policy_master_plan.plan_7, policy_master_plan.plan_8, policy_master_plan.plan_9, policy_master_plan.plan_10]
								for pl_list in range(10):
									if mother_plan_list[pl_list]:
										if str(plan_list[pl_list]) < str(mother_plan_list[pl_list]):
											frappe.throw(f"{policy_master_plan.policy_benefits} has higher amount in option than Mother Policy.")
		
		


	def increase_decrease_value(self, mother_policy):
		if len(self.policy_premium)>0:
			for pol_prem in range(len(mother_policy.policy_premium)):
				for prem in self.policy_premium:
					if prem.update_by:
						if prem.update_type == "Increase":
							if prem.update_amount_type == "Percentage":
								# Increase the premium amount in Percentage
								if prem.maximum_trip_duration == mother_policy.policy_premium[pol_prem].maximum_trip_duration:
									prem.plan_1 = float(mother_policy.policy_premium[pol_prem].plan_1) + (float(mother_policy.policy_premium[pol_prem].plan_1)/100*float(prem.update_by))
									prem.plan_2 = float(mother_policy.policy_premium[pol_prem].plan_2) + (float(mother_policy.policy_premium[pol_prem].plan_2)/100*float(prem.update_by))
									prem.plan_3 = float(mother_policy.policy_premium[pol_prem].plan_3) + (float(mother_policy.policy_premium[pol_prem].plan_3)/100*float(prem.update_by))
									prem.plan_4 = float(mother_policy.policy_premium[pol_prem].plan_4) + (float(mother_policy.policy_premium[pol_prem].plan_4)/100*float(prem.update_by))
									prem.plan_5 = float(mother_policy.policy_premium[pol_prem].plan_5) + (float(mother_policy.policy_premium[pol_prem].plan_5)/100*float(prem.update_by))
									prem.plan_6 = float(mother_policy.policy_premium[pol_prem].plan_6) + (float(mother_policy.policy_premium[pol_prem].plan_6)/100*float(prem.update_by))
									prem.plan_7 = float(mother_policy.policy_premium[pol_prem].plan_7) + (float(mother_policy.policy_premium[pol_prem].plan_7)/100*float(prem.update_by))
									prem.plan_8 = float(mother_policy.policy_premium[pol_prem].plan_8) + (float(mother_policy.policy_premium[pol_prem].plan_8)/100*float(prem.update_by))
									prem.plan_9 = float(mother_policy.policy_premium[pol_prem].plan_9) + (float(mother_policy.policy_premium[pol_prem].plan_9)/100*float(prem.update_by))
									prem.plan_10 = float(mother_policy.policy_premium[pol_prem].plan_10) + (float(mother_policy.policy_premium[pol_prem].plan_10)/100*float(prem.update_by))
							elif prem.update_amount_type == "Amount":
								# Increase the premium amount in Amount
								if prem.maximum_trip_duration == mother_policy.policy_premium[pol_prem].maximum_trip_duration:
									# Check if the premium amount is 0.0 or else add update amount
									if float(prem.plan_1) != 0.0: prem.plan_1 = float(mother_policy.policy_premium[pol_prem].plan_1) + float(prem.update_by)
									if float(prem.plan_2) != 0.0: prem.plan_2 = float(mother_policy.policy_premium[pol_prem].plan_2) + float(prem.update_by)
									if float(prem.plan_3) != 0.0: prem.plan_3 = float(mother_policy.policy_premium[pol_prem].plan_3) + float(prem.update_by)
									if float(prem.plan_4) != 0.0: prem.plan_4 = float(mother_policy.policy_premium[pol_prem].plan_4) + float(prem.update_by)
									if float(prem.plan_5) != 0.0: prem.plan_5 = float(mother_policy.policy_premium[pol_prem].plan_5) + float(prem.update_by)
									if float(prem.plan_6) != 0.0: prem.plan_6 = float(mother_policy.policy_premium[pol_prem].plan_6) + float(prem.update_by)
									if float(prem.plan_7) != 0.0: prem.plan_7 = float(mother_policy.policy_premium[pol_prem].plan_7) + float(prem.update_by)
									if float(prem.plan_8) != 0.0: prem.plan_8 = float(mother_policy.policy_premium[pol_prem].plan_8) + float(prem.update_by)
									if float(prem.plan_9) != 0.0: prem.plan_9 = float(mother_policy.policy_premium[pol_prem].plan_9) + float(prem.update_by)
									if float(prem.plan_10) != 0.0: prem.plan_10 = float(mother_policy.policy_premium[pol_prem].plan_10) + float(prem.update_by)
						if prem.update_type == "Decrease":
							if prem.update_amount_type == "Precentage":
								# Decrease the premium amount in Percentage amount
								if prem.maximum_trip_duration == mother_policy.policy_premium[pol_prem].maximum_trip_duration:
									prem.plan_1 = float(mother_policy.policy_premium[pol_prem].plan_1) - (float(mother_policy.policy_premium[pol_prem].plan_1)/100*float(prem.update_by))
									prem.plan_2 = float(mother_policy.policy_premium[pol_prem].plan_2) - (float(mother_policy.policy_premium[pol_prem].plan_2)/100*float(prem.update_by))
									prem.plan_3 = float(mother_policy.policy_premium[pol_prem].plan_3) - (float(mother_policy.policy_premium[pol_prem].plan_3)/100*float(prem.update_by))
									prem.plan_4 = float(mother_policy.policy_premium[pol_prem].plan_4) - (float(mother_policy.policy_premium[pol_prem].plan_4)/100*float(prem.update_by))
									prem.plan_5 = float(mother_policy.policy_premium[pol_prem].plan_5) - (float(mother_policy.policy_premium[pol_prem].plan_5)/100*float(prem.update_by))
									prem.plan_6 = float(mother_policy.policy_premium[pol_prem].plan_6) - (float(mother_policy.policy_premium[pol_prem].plan_6)/100*float(prem.update_by))
									prem.plan_7 = float(mother_policy.policy_premium[pol_prem].plan_7) - (float(mother_policy.policy_premium[pol_prem].plan_7)/100*float(prem.update_by))
									prem.plan_8 = float(mother_policy.policy_premium[pol_prem].plan_8) - (float(mother_policy.policy_premium[pol_prem].plan_8)/100*float(prem.update_by))
									prem.plan_9 = float(mother_policy.policy_premium[pol_prem].plan_9) - (float(mother_policy.policy_premium[pol_prem].plan_9)/100*float(prem.update_by))
									prem.plan_10 = float(mother_policy.policy_premium[pol_prem].plan_10) - (float(mother_policy.policy_premium[pol_prem].plan_10)/100*float(prem.update_by))
							elif prem.update_amount_type == "Amount":
								# Decrease the premium amount in Amount
								if prem.maximum_trip_duration == mother_policy.policy_premium[pol_prem].maximum_trip_duration:
									# Check if the premium amount is 0 or else minus update amount from premium
									if float(prem.plan_1) != 0.0: prem.plan_1 = float(mother_policy.policy_premium[pol_prem].plan_1) - float(prem.update_by)
									if float(prem.plan_2) != 0.0: prem.plan_2 = float(mother_policy.policy_premium[pol_prem].plan_2) - float(prem.update_by)
									if float(prem.plan_3) != 0.0: prem.plan_3 = float(mother_policy.policy_premium[pol_prem].plan_3) - float(prem.update_by)
									if float(prem.plan_4) != 0.0: prem.plan_4 = float(mother_policy.policy_premium[pol_prem].plan_4) - float(prem.update_by)
									if float(prem.plan_5) != 0.0: prem.plan_5 = float(mother_policy.policy_premium[pol_prem].plan_5) - float(prem.update_by)
									if float(prem.plan_6) != 0.0: prem.plan_6 = float(mother_policy.policy_premium[pol_prem].plan_6) - float(prem.update_by)
									if float(prem.plan_7) != 0.0: prem.plan_7 = float(mother_policy.policy_premium[pol_prem].plan_7) - float(prem.update_by)
									if float(prem.plan_8) != 0.0: prem.plan_8 = float(mother_policy.policy_premium[pol_prem].plan_8) - float(prem.update_by)
									if float(prem.plan_9) != 0.0: prem.plan_9 = float(mother_policy.policy_premium[pol_prem].plan_9) - float(prem.update_by)
									if float(prem.plan_10) != 0.0: prem.plan_10 = float(mother_policy.policy_premium[pol_prem].plan_10) - float(prem.update_by)
						
		# Update Policy Premium amount in every row
		if self.update_type == "Increase":
			if self.update_amount_type == "Percentage":
				for premium in range(len(mother_policy.policy_premium)):
					for prem in self.policy_premium:
						if not prem.update_by:
							if prem.maximum_trip_duration == mother_policy.policy_premium[premium].maximum_trip_duration:
								prem.plan_1 = float(mother_policy.policy_premium[premium].plan_1) + (float(mother_policy.policy_premium[premium].plan_1)/100*float(self.update_amount))
								prem.plan_2 = float(mother_policy.policy_premium[premium].plan_2) + (float(mother_policy.policy_premium[premium].plan_2)/100*float(self.update_amount))
								prem.plan_3 = float(mother_policy.policy_premium[premium].plan_3) + (float(mother_policy.policy_premium[premium].plan_3)/100*float(self.update_amount))
								prem.plan_4 = float(mother_policy.policy_premium[premium].plan_4) + (float(mother_policy.policy_premium[premium].plan_4)/100*float(self.update_amount))
								prem.plan_5 = float(mother_policy.policy_premium[premium].plan_5) + (float(mother_policy.policy_premium[premium].plan_5)/100*float(self.update_amount))
								prem.plan_6 = float(mother_policy.policy_premium[premium].plan_6) + (float(mother_policy.policy_premium[premium].plan_6)/100*float(self.update_amount))
								prem.plan_7 = float(mother_policy.policy_premium[premium].plan_7) + (float(mother_policy.policy_premium[premium].plan_7)/100*float(self.update_amount))
								prem.plan_8 = float(mother_policy.policy_premium[premium].plan_8) + (float(mother_policy.policy_premium[premium].plan_8)/100*float(self.update_amount))
								prem.plan_9 = float(mother_policy.policy_premium[premium].plan_9) + (float(mother_policy.policy_premium[premium].plan_9)/100*float(self.update_amount))
								prem.plan_10 = float(mother_policy.policy_premium[premium].plan_10) + (float(mother_policy.policy_premium[premium].plan_10)/100*float(self.update_amount))
			elif self.update_amount_type == "Amount":
				for premium in range(len(mother_policy.policy_premium)):
					for prem in self.policy_premium:
						if not prem.update_by:
							if prem.maximum_trip_duration == mother_policy.policy_premium[premium].maximum_trip_duration:
								if float(prem.plan_1) != 0.0: prem.plan_1 = float(mother_policy.policy_premium[premium].plan_1) + float(self.update_amount)
								if float(prem.plan_2) != 0.0: prem.plan_2 = float(mother_policy.policy_premium[premium].plan_2) + float(self.update_amount)
								if float(prem.plan_3) != 0.0: prem.plan_3 = float(mother_policy.policy_premium[premium].plan_3) + float(self.update_amount)
								if float(prem.plan_4) != 0.0: prem.plan_4 = float(mother_policy.policy_premium[premium].plan_4) + float(self.update_amount)
								if float(prem.plan_5) != 0.0: prem.plan_5 = float(mother_policy.policy_premium[premium].plan_5) + float(self.update_amount)
								if float(prem.plan_6) != 0.0: prem.plan_6 = float(mother_policy.policy_premium[premium].plan_6) + float(self.update_amount)
								if float(prem.plan_7) != 0.0: prem.plan_7 = float(mother_policy.policy_premium[premium].plan_7) + float(self.update_amount)
								if float(prem.plan_8) != 0.0: prem.plan_8 = float(mother_policy.policy_premium[premium].plan_8) + float(self.update_amount)
								if float(prem.plan_9) != 0.0: prem.plan_9 = float(mother_policy.policy_premium[premium].plan_9) + float(self.update_amount)
								if float(prem.plan_10) != 0.0: prem.plan_10 = float(mother_policy.policy_premium[premium].plan_10) + float(self.update_amount)
		elif self.update_type == "Decrease":
			if self.update_amount_type == "Percentage":
				for premium in range(len(mother_policy.policy_premium)):
					for prem in self.policy_premium:
						if not prem.update_by:
							if prem.maximum_trip_duration == mother_policy.policy_premium[premium].maximum_trip_duration:
								prem.plan_1 = float(mother_policy.policy_premium[premium].plan_1) - (float(mother_policy.policy_premium[premium].plan_1)/100*float(self.update_amount))
								prem.plan_2 = float(mother_policy.policy_premium[premium].plan_2) - (float(mother_policy.policy_premium[premium].plan_2)/100*float(self.update_amount))
								prem.plan_3 = float(mother_policy.policy_premium[premium].plan_3) - (float(mother_policy.policy_premium[premium].plan_3)/100*float(self.update_amount))
								prem.plan_4 = float(mother_policy.policy_premium[premium].plan_4) - (float(mother_policy.policy_premium[premium].plan_4)/100*float(self.update_amount))
								prem.plan_5 = float(mother_policy.policy_premium[premium].plan_5) - (float(mother_policy.policy_premium[premium].plan_5)/100*float(self.update_amount))
								prem.plan_6 = float(mother_policy.policy_premium[premium].plan_6) - (float(mother_policy.policy_premium[premium].plan_6)/100*float(self.update_amount))
								prem.plan_7 = float(mother_policy.policy_premium[premium].plan_7) - (float(mother_policy.policy_premium[premium].plan_7)/100*float(self.update_amount))
								prem.plan_8 = float(mother_policy.policy_premium[premium].plan_8) - (float(mother_policy.policy_premium[premium].plan_8)/100*float(self.update_amount))
								prem.plan_9 = float(mother_policy.policy_premium[premium].plan_9) - (float(mother_policy.policy_premium[premium].plan_9)/100*float(self.update_amount))
								prem.plan_10 = float(mother_policy.policy_premium[premium].plan_10) - (float(mother_policy.policy_premium[premium].plan_10)/100*float(self.update_amount))
			elif self.update_amount_type == "Amount":
				for premium in range(len(mother_policy.policy_premium)):
					for prem in self.policy_premium:
						if not prem.update_by:
							if prem.maximum_trip_duration == mother_policy.policy_premium[premium].maximum_trip_duration:
								if float(prem.plan_1) != 0.0: prem.plan_1 = float(mother_policy.policy_premium[premium].plan_1) - float(self.update_amount)
								if float(prem.plan_2) != 0.0: prem.plan_2 = float(mother_policy.policy_premium[premium].plan_2) - float(self.update_amount)
								if float(prem.plan_3) != 0.0: prem.plan_3 = float(mother_policy.policy_premium[premium].plan_3) - float(self.update_amount)
								if float(prem.plan_4) != 0.0: prem.plan_4 = float(mother_policy.policy_premium[premium].plan_4) - float(self.update_amount)
								if float(prem.plan_5) != 0.0: prem.plan_5 = float(mother_policy.policy_premium[premium].plan_5) - float(self.update_amount)
								if float(prem.plan_6) != 0.0: prem.plan_6 = float(mother_policy.policy_premium[premium].plan_6) - float(self.update_amount)
								if float(prem.plan_7) != 0.0: prem.plan_7 = float(mother_policy.policy_premium[premium].plan_7) - float(self.update_amount)
								if float(prem.plan_8) != 0.0: prem.plan_8 = float(mother_policy.policy_premium[premium].plan_8) - float(self.update_amount)
								if float(prem.plan_9) != 0.0: prem.plan_9 = float(mother_policy.policy_premium[premium].plan_9) - float(self.update_amount)
								if float(prem.plan_10) != 0.0: prem.plan_10 = float(mother_policy.policy_premium[premium].plan_10) - float(self.update_amount)
						

	def after_insert(self):
		if self.package_policy == 1:
			if len(self.parent_policy_table)>0:
				self.insurance_plan_details.clear()
				self.policy_premium.clear()
				self.activity_list.clear()
				primary = False
				age_val = 0
				for parent in self.parent_policy_table:
					parent_policy = get_doc("Mother Policy", parent.parent_policy)
					if parent_policy.max_age_limit and parent_policy.min_age_limit:
						age_cal = float(parent_policy.max_age_limit) - float(parent_policy.min_age_limit)
						if age_cal>age_val:
							age_val = age_cal
							self.min_age_limit = parent_policy.min_age_limit
							self.max_age_limit = parent_policy.max_age_limit

					if parent.primary == 1:
						if not primary:
							primary = True
							self.scope_of_policy = parent_policy.scope_of_policy
							self.type_of_policy = parent_policy.type_of_policy
						else:
							frappe.throw("You can only select one primary Mother Policy.")
					for plan in parent_policy.insurance_plan_details:
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
							"deductible": plan.deductible
						})
					for premium in parent_policy.policy_premium:
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
						})
					for activity in parent_policy.activity_list:
						self.append("activity_list", {
							"activity_name": activity.activity_name,
							"level": activity.level,
							"mother_policy_level": activity.mother_policy_level,
							"category": activity.category
						})
				
				if not primary:
					frappe.throw("Please select one primary Mother Policy")
		self.save()