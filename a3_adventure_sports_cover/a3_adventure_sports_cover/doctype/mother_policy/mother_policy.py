# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

from dataclasses import fields
from warnings import filters
import frappe
from frappe import get_list, new_doc, get_doc, get_value
from frappe.model.document import Document
from datetime import datetime, timedelta

class MotherPolicy(Document):
	def on_submit(self):
		for premium in self.policy_premium:
			policy_premium_item = new_doc("Policy Premium Items")
			policy_premium_item.plan_name = self.name
			policy_premium_item.name = f"{self.name}/{premium.maximum_trip_duration} Days(s)"
			policy_premium_item.maximum_trip_duration = premium.maximum_trip_duration
			policy_premium_item.plan_1 = premium.plan_1
			policy_premium_item.plan_2 = premium.plan_2
			policy_premium_item.plan_3 = premium.plan_3
			policy_premium_item.plan_4 = premium.plan_4
			policy_premium_item.plan_5 = premium.plan_5
			policy_premium_item.plan_6 = premium.plan_6
			policy_premium_item.plan_7 = premium.plan_7
			policy_premium_item.plan_8 = premium.plan_8
			policy_premium_item.plan_9 = premium.plan_9
			policy_premium_item.plan_10 = premium.plan_10
		
			policy_premium_item.insert()
			frappe.db.commit()

	def before_update_after_submit(self):
		old_fiscal_year = get_value("Mother Policy", self.name, "financial_year")
		fiscal_year = get_doc("Fiscal Year", old_fiscal_year)

		sdate = fiscal_year.year_start_date   #first date of the month
		edate = fiscal_year.year_end_date  #Last date of the month
		date_modified = sdate
		date_list = [sdate]
		today = datetime.today().date()

		# get all dates between two start date and end date
		while date_modified < edate:
			date_modified += timedelta(days=1)
			date_list.append(date_modified)

		if today in date_list:
			frappe.throw("You can change financial year until current financial year is not over.")

	
	def on_update_after_submit(self):
		
		# Get current fiscal year start date and end date
		# fiscal_year = frappe.get_doc("Fiscal Year", {"disabled":0})
		# sdate = fiscal_year.year_start_date   #first date of the month
		# edate = fiscal_year.year_end_date  #Last date of the month
		# date_modified = sdate
		# date_list = [sdate]
		# issue_date = self.date_of_issue

		# if isinstance(issue_date, str):
		# 	issue_date = dt.strptime(issue_date, "%Y-%m-%d").date()


		# # get all dates between two start date and end date
		# while date_modified<edate:
		# 	date_modified+=timedelta(days=1)
		# 	date_list.append(date_modified)









		# If Mother Policy is made inactive it will turn Policy Master and its corresponding Customised Policy inactive and vice a versa
		policy_master_list = get_list("Policy Master")
		if self.status == "Inactive":
			for policy_master in policy_master_list:
				policy = get_doc("Policy Master", policy_master.name)
				if policy.parent_policy == self.name:
					customised_policy = get_list("Customised Policy", filters = {"parent_policy": policy.name})
					for custom in customised_policy:
						custom_policy = get_doc("Customised Policy", custom.name)
						custom_policy.status = "Inactive"
						custom_policy.db_update()

						plan_list = frappe.get_list("Item", filters={"parent_policy": custom_policy.name})
						for item in plan_list:
							it = frappe.get_doc("Item", item.name)
							it.disabled = 1
							it.save()
					policy.status = "Inactive"
					policy.db_update()
		else:
			for policy_master in policy_master_list:
				policy = get_doc("Policy Master", policy_master.name)
				if policy.parent_policy == self.name:
					customised_policy = get_list("Customised Policy", filters = {"parent_policy": policy.name})
					for custom in customised_policy:
						custom_policy = get_doc("Customised Policy", custom.name)
						custom_policy.status = "Active"
						custom_policy.db_update()
						plan_list = frappe.get_list("Item", filters={"parent_policy": custom_policy.name})
						for item in plan_list:
							it = frappe.get_doc("Item", item.name)
							it.disabled = 0
							it.save()
					policy.status = "Active"
					policy.db_update()

	def after_insert(self):
		self.activity_list.clear()
		if self.level_1 == 1:
			activities = get_list("Activity Master", filters={"activity_level":"Level 1"})
			provider_level = ""
			for activity in activities:
				act = get_doc("Activity Master", activity["name"])
				# print(act.as_dict())
				for pro_level in act.levels_of_activity:
					if pro_level.policy_provider == self.policy_provider:
						provider_level = pro_level.level
				self.append("activity_list", {
					"activity_name": act.activity_name,
					"level": act.activity_level,
			 		"category": act.activity_category,
			 		"mother_policy_level": provider_level
				})
			# for activity in activities:
			# 	act = get_doc("Activity Master", activity["activity_name"])
			# 	print(act.level_list)
			# 	for pro_level in act.level_list:
			# 		if pro_level.policy_provider == self.policy_provider:
			# 			provider_level = pro_level.level
			# 	self.append("activity_list",{
			# 		"activity_name": activity["activity_name"],
			# 		"level": activity["activity_level"],
			# 		"category": activity["activity_category"],
			# 		"mother_policy_level": provider_level
			# 	})
		if self.level_2 == 1:
			activities = get_list("Activity Master", filters={"activity_level":"Level 2"})
			provider_level = ""
			for activity in activities:
				act = get_doc("Activity Master", activity["name"])
				# print(act.as_dict())
				for pro_level in act.levels_of_activity:
					if pro_level.policy_provider == self.policy_provider:
						provider_level = pro_level.level
				self.append("activity_list", {
					"activity_name": act.activity_name,
					"level": act.activity_level,
			 		"category": act.activity_category,
			 		"mother_policy_level": provider_level
				})
		if self.level_3 == 1:
			activities = get_list("Activity Master", filters={"activity_level":"Level 3"})
			provider_level = ""
			for activity in activities:
				act = get_doc("Activity Master", activity["name"])
				# print(act.as_dict())
				for pro_level in act.levels_of_activity:
					if pro_level.policy_provider == self.policy_provider:
						provider_level = pro_level.level
				self.append("activity_list", {
					"activity_name": act.activity_name,
					"level": act.activity_level,
			 		"category": act.activity_category,
			 		"mother_policy_level": provider_level
				})
		if self.level_4 == 1:
			activities = get_list("Activity Master", filters={"activity_level":"Level 4"})
			provider_level = ""
			for activity in activities:
				act = get_doc("Activity Master", activity["name"])
				# print(act.as_dict())
				for pro_level in act.levels_of_activity:
					if pro_level.policy_provider == self.policy_provider:
						provider_level = pro_level.level
				self.append("activity_list", {
					"activity_name": act.activity_name,
					"level": act.activity_level,
			 		"category": act.activity_category,
			 		"mother_policy_level": provider_level
				})
		if self.level_5 == 1:
			activities = get_list("Activity Master", filters={"activity_level":"Level 5"})
			provider_level = ""
			for activity in activities:
				act = get_doc("Activity Master", activity["name"])
				# print(act.as_dict())
				for pro_level in act.levels_of_activity:
					if pro_level.policy_provider == self.policy_provider:
						provider_level = pro_level.level
				self.append("activity_list", {
					"activity_name": act.activity_name,
					"level": act.activity_level,
			 		"category": act.activity_category,
			 		"mother_policy_level": provider_level
				})
		self.save()