from frappe import get_doc, msgprint
import frappe
from frappe.model.mapper import get_mapped_doc


def on_submit(doc, event):

	#This loop will create Operator Plocy Issued for every passengers in Booking.

	for passenger in range(len(doc.booking_passengers)):
		issue = get_doc({

			'doctype': 'Operator Policy Issued',

			# Passenger Details
			'name1': doc.booking_passengers[passenger].passenger_name,
			'dob': doc.booking_passengers[passenger].date_of_birth,
			'gender': doc.booking_passengers[passenger].gender,
			'email_id': doc.booking_passengers[passenger].email_id,
			'contact': doc.booking_passengers[passenger].contact_number,
			'address': doc.booking_passengers[passenger].address,
			'nationality': doc.booking_passengers[passenger].nationality,
			'pan_number': doc.booking_passengers[passenger].pan_number,
			'aadhaar_number': doc.booking_passengers[passenger].aadhaar_number,
			'passport_number':doc.booking_passengers[passenger].passport_number,

			#Other Details
			'pre_existing_disease': doc.booking_passengers[passenger].pre_existing_disease,
			'are_you_club_member_of_organizing_committee': doc.booking_passengers[passenger].are_you_club_member_of_organizing_committee,
			'experience_with_the_sport_or_activity': doc.booking_passengers[passenger].experience_with_the_sport_or_activity,
			'number_of_years_of_experience_with_the_sport_or_activity': doc.booking_passengers[passenger].number_of_years_of_experience_with_the_sport_or_activity,
			'have_you_obtained_fitness_certificate': doc.booking_passengers[passenger].have_you_obtained_fitness_certificate,
			'details_of_pre_existing_disease': doc.booking_passengers[passenger].details_of_pre_existing_disease,
			'name_of_the_sport_equipment_used_in_sport_activity': doc.booking_passengers[passenger].name_of_the_sport_equipment_used_in_sport_activity,
			'proficiency_level': doc.booking_passengers[passenger].proficiency_level,

			#Product Details
			'operator': doc.operator,
			'operator_product': doc.operator_product,
			'booking_date': doc.booking_date,
			'nature_of_activity': doc.nature_of_activity,
			'any_previous_insurance_ever_been_declined': doc.any_previous_insurance_ever_been_declined,
			'time_of_day_of_activity': doc.time_of_day_of_activity,
			'activity_date': doc.activity_date,
			'doctor_or_medical_practitioner_on_site': doc.doctor_or_medical_practitioner_on_site,
			'manager_or_trainer_to_group_members_ratio': doc.manager_or_trainer_to_group_members_ratio,
			
			#Nominee Details
			'nominee_name': doc.booking_passengers[passenger].nominee_name,
			'nominee_contact_number': doc.booking_passengers[passenger].nominee_contact_number,
			'nominee_relationship': doc.booking_passengers[passenger].nominee_relationship,

			#Transportation Details
			'transportation_type': doc.transportation_type,
			'specifications': doc.specifications,

			# Policy Details
			'activity': doc.activity,
			'premium': doc.premium,
			'end_date': doc.end_date,
			'period_of_issuance': doc.period_of_issuance,
			'policy': doc.policy,
			'start_date': doc.start_date,
			'policy_provider': doc.policy_provider
		})

		#Eqiupment Details
		for equipment in range(len(doc.booking_equipments)):
			issue.append('operator_equipment', {
					'equipment': doc.booking_equipments[equipment].equipment,
					'activity_name':doc.booking_equipments[equipment].activity_name,
					'max_capacity':doc.booking_equipments[equipment].max_capacity,
					'min_capacity':doc.booking_equipments[equipment].min_capacity,
					'model_number':doc.booking_equipments[equipment].model_number,
					'hours_clocked':doc.booking_equipments[equipment].hours_clocked,
				})

		#Staff Details
		for staff in range(len(doc.booking_staff)):
			issue.append("operator_staff", {
				'staff_name': doc.booking_staff[staff].staff_name,
				'activity_name': doc.booking_staff[staff].activity_name,
				'license_expiry_date': doc.booking_staff[staff].license_expiry_date
			})
		issue.insert()
	msgprint("Policy created.")