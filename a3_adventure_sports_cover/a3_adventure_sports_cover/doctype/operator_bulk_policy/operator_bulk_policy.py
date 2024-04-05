# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

from frappe import new_doc, local
from datetime import datetime
from frappe.model.document import Document
from pandas import ExcelFile
from numpy import nan

class OperatorBulkPolicy(Document):
	def after_insert(self):
		site = local.request.host
		xls = ExcelFile(f'http://{site}{self.attach_excel}')
		df = xls.parse(xls.sheet_names[0])
		df.fillna("", inplace=True)
		df = df.to_dict()
		bulk_doc = new_doc("B2B Policy Issue")
		bulk_doc.policy_type = "Bulk Policy"
		bulk_doc.operator = self.operator
		bulk_doc.operator_email = self.email
		bulk_doc.operator_email_preference = self.email_preference
		bulk_doc.start_date = self.start_journey
		bulk_doc.end_date = self.end_journey
		bulk_doc.policy_name = self.policy_name
		bulk_doc.policy = self.plan_name
		bulk_doc.period_of_issuance = self.maximum_trip_duration
		bulk_doc.amount = self.premium_amount
		bulk_doc.send_whatsapp_alert = self.send_whatsapp_alert
		for i in range(len(df["Customer Name"])):
			print(df["Flight Number"][i])
			date_of_birth = df["Date of Birth"][i]
			if isinstance(date_of_birth, str):
				date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y").date()
			bulk_doc.append("bulk_upload",{
				"name1": df["Customer Name"][i],
				"gender": df["Gender"][i],
				"date_of_birth": date_of_birth,
				"email_id": df["Email ID"][i],
				"contact": df["Contact"][i],
				"address": df["Address"][i],
				"event": df["Event"][i],
				"pan_number": df["PAN Number"][i],
				"aadhar_number": df["Aadhar Number"][i],
				"passport_number": df["Passport Number"][i],
				"nominee_name": df["Nominee Name"][i],
				"nominee_contact": df["Nominee Contact"][i],
				"nominee_relationship": df["Nominee Relationship"][i],
				"nationality": df["Nationality"][i],
				"ref1": df["Ref1"][i],
				"ref2": df["Ref2"][i],
				"ref3": df["Ref3"][i],
				"flight_number": df["Flight Number"][i],
				"flight_departure_code": df["Flight Departure Code"][i],
				"flight_arrival_code": df["Flight Arrival Code"][i],
				"departure_date": df["Departure Date"][i],
				"departure_time": df["Departure Time"][i],
				"arrival_date": df["Arrival Date"][i],
				"arrival_time": df["Arrival Time"][i],
				"trip_type": df["Trip Type"][i],
				"maximum_trip_duration": df["Maximum Trip Duration"][i],
				"employee_number": df["Employee Number"][i],
				"department_name": df["Department Name"][i],
				"pan_no_national_id_no": df["PAN No National ID No"][i],
				"residential_status": df["Residential Status"][i],
				"country_of_issue_of_passport": df["Country of Issue of Passport"][i],
				"common_carrier_or_public_carrier_opted": df["Common Carrier or Public Carrier Opted"][i],
				"adventure_sport_activities_on_trip": df["Adventure Sport Activities on Trip"][i],
				"detailed_itineary_of_the_trip": df["Detailed Itineary of The Trip"][i],
				"debit__or_credit_card_no": df["Debit  or Credit Card No"][i],
				"guardian_name": df["Guardian Name"][i],
				"assignee_name": df["Assignee Name"][i],
				"nominee_date_of_birth": df["Nominee Date of Birth"][i],
				"name_of_university": df["Name of University"][i],
				"course_name": df["Course Name"][i],
				"university_address": df["University Address"][i],
				"university_city": df["University City"][i],
				"university_state": df["University State"][i],
				"university_country": df["University Country"][i],
				"sponsor_name": df["Sponsor Name"][i],
				"sponsor_relationship_to_insured": df["Sponsor Relationship to Insured"][i],
				"sponsor_address": df["Sponsor Address"][i],
				"sponsor_date_of_birth": df["Sponsor Date of Birth"][i],
				"sponsor_contact_number": df["Sponsor Contact Number"][i]
			})
		bulk_doc.save()
		bulk_doc.submit()