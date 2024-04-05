import frappe
import boto3
import json
from datetime import datetime
import hashlib
import random
import string
import base64
from pyqrcode import create as qrcreate
import io
import os
import requests as req
from frappe.model.document import Document
import datetime
from datetime import datetime as dt


class OperatorPolicyIssued(Document):
    # def __init__(self):
    #     """
    #          Function to initialise the aws settings from frappe S3 File attachment
    #          doctype.
    #          """
    #     self.s3_settings_doc = frappe.get_doc(
    #         'S3 File Attachment',
    #         'S3 File Attachment',
    #     )
    #     if (
    #             self.s3_settings_doc.aws_key and
    #             self.s3_settings_doc.aws_secret
    #     ):
    #         self.S3_CLIENT = boto3.client(
    #             's3',
    #             aws_access_key_id=self.s3_settings_doc.aws_key,
    #             aws_secret_access_key=self.s3_settings_doc.aws_secret,
    #             region_name=self.s3_settings_doc.region_name,
    #         )
    #     else:
    #         self.S3_CLIENT = boto3.client('s3')
    #     self.BUCKET = self.s3_settings_doc.bucket_name
    #     self.folder_name = self.s3_settings_doc.folder_name

    def before_insert(self):
        #Naming Series
        if self.endorsed == 0:
            if self.policy:
                pol = frappe.get_doc("Item",self.policy)
                if pol.master_policy:
                    master = frappe.get_doc("Policy Master",pol.master_policy)
                    if master.scope_of_policy:
                        scope = master.scope_of_policy
                        if scope == "International":
                            scope_id = "I"
                        elif scope == "Domestic":
                            scope_id = "D"
                    if master.type_of_policy:
                        type = master.type_of_policy
                        if type == "Short Term":
                            type_id = "S"
                        elif type == "Annual":
                            type_id = "A"
                    if master.policy_provider:
                        provider = master.policy_provider
                        provider_id = provider[0]

            operator_code = frappe.get_value("Operator", self.operator, "operator_code")
                        
            today = dt.today()
            policy_list = frappe.get_list("List of Policy")
            if len(policy_list)==0:
                series_no = 0
            else:
                last_doc = frappe.get_last_doc("List of Policy")
                series_no = int(last_doc.series_number)+1
            if scope and type and provider:
                policy_number = f"ASC360-{scope_id}{type_id}{provider_id}{operator_code}-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"
            else:
                policy_number = f"ASC360-MDBK{operator_code}-{today.month}-{today.year}-PI{'{:05d}'.format(series_no)}"

            self.policy_number = policy_number
        else:
            # policy = frappe.get_value("Endorsement Form", self.endorsement, "original_policy")
            self.policy_number = f"{self.original_policy} - {self.endorsement_count}"

        #PDF Generation

        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=17))
        s3_key_name_hash = hashlib.sha256(str(self.name).encode() + str(self.email_id).encode() + str(res).encode())

        if not s3_key_name_hash:
            frappe.throw("Unable to Create s3 name")

        s3_file_name = dt.now().strftime('%h-%Y').lower() + "-" + s3_key_name_hash.hexdigest()
        self.unique_hash        = str(s3_file_name)
        self.verification_url   = "https://verify.djiboutiimmigration.com?id="+s3_file_name
        self.qrcode_path        = self.generate_qrcode()

    def on_submit(self):

        # values = {
        #     "name": self.name,
        #     "creation": self.creation,
        #     "date_of_issue": self.date_of_issue,
        #     "full_name": self.full_name,
        #     "nationality": self.nationality,
        #     "email_id": self.email_id,
        #     "date_of_birth": self.date_of_birth,
        #     "address": self.address,
        #     "passport_number": self.passport_number,
		# 	"nominee_name": self.nominee_name,
		# 	"nominee_contact_number": self.nominee_contact_number,
		# 	"nominee_relationship": self.nominee_relationship,
		# 	"pre_existing_disease": self.pre_existing_disease,
		# 	"are_you_club_member_of_organizing_committee": self.are_you_club_member_of_organizing_committee,
		# 	"experience_with_the_sport_or_activity": self.experience_with_the_sport_or_activity,
		# 	"number_of_years_of_experience_with_the_sport_or_activity": self.number_of_years_of_experience_with_the_sport_or_activity,
		# 	"have_you_obtained_fitness_certificate": self.have_you_obtained_fitness_certificate,
		# 	"details_of_pre_existing_disease": self.details_of_pre_existing_disease,
		# 	"name_of_the_sport_equipment_used_in_sport_activity": self.name_of_the_sport_equipment_used_in_sport_activity,
		# 	"proficiency_level": self.proficiency_level,
		# 	"nature_of_activity": self.nature_of_activity,
		# 	"any_previous_insurance_ever_been_declined": self.any_previous_insurance_ever_been_declined,
		# 	"time_of_day_of_activity": self.time_of_day_of_activity,
		# 	"doctor_or_medical_practitioner_on_site": self.doctor_or_medical_practitioner_on_site,
		# 	"manager_or_trainer_to_group_members_ratio": self.manager_or_trainer_to_group_members_ratio,
		# 	"activity": self.activity,
		# 	"policy": self.policy,
		# 	"policy_provider": self.policy_provider,
		# 	"premium": self.premium,
		# 	"period_of_issuance": self.period_of_issuance
        # }


      

        invoice = frappe.new_doc("Sales Invoice")
        invoice.customer = self.name1
        invoice.due_date = self.date_of_issue
        invoice.operator = self.operator
        invoice.sales_partner = self.operator
        invoice.append(
            "items",
            {
                "item_code": self.policy,
                "rate": self.premium
            },
        )
        invoice.set_missing_values()
        # invoice.insert()
        invoice.submit()
        frappe.msgprint("Sales Invoice generated & Submitted successfully")

        if self.operator:
            op = self.operator
            if frappe.db.exists("Operator Balance",op):
                bal = frappe.get_doc("Operator Balance",op)
                if bal.number_of_policy_issued:
                    no = int(bal.number_of_policy_issued)
                    nos = no + 1
                    bal.number_of_policy_issued = float(nos)
                    bal.total_policy_amount = float(bal.total_policy_amount) + float(self.premium)
                    bal.balance_available = float(bal.invoice_amount) - float(bal.total_policy_amount)
                # else:
                #     bal.number_of_policy_issued =1
                #     bal.total_policy_amount = self.premium 
                #     amt =  float(bal.invoice_amount)
                #     bal.balance_available = amt - prem 
                bal.save()

        #Create Operator Balance Receivable
        if self.premium:
            if self.operator:
                operator = frappe.get_doc("Operator",self.operator)
                if operator.commisson_type:
                    if operator.commisson_type == "Percentage":
                        if operator.commission_percentage:
                            perc = operator.commission_percentage

                            #Calculate Commission
                            amount = self.premium
                            commission = (float(amount) * float(perc))/100
                #Insert Operator Commission Receivable
                if commission:
                    com = frappe.new_doc("Operator Commission Payable")
                    com.operator = self.operator
                    com.policy = "Operator Policy Issued"
                    com.policy_number = self.name
                    com.policy_date = self.date_of_issue
                    com.commission_payable = commission 
                    com.insert()
                    frappe.msgprint("Operator Commission Saved!!")

                    #Create Invoice for Operator Commission to pe Paid
                    inv = frappe.new_doc("Sales Invoice")
                    inv.customer = self.operator
                    inv.due_date = self.date_of_issue
                    inv.append(
                        "items",
                    {
                        "item_code":"COM",
                        "item_name": "Commission",
                        "qty": 1,
                        "rate": commission
                    })
                    inv.set_missing_values()
                    inv.insert()
                    inv.submit()
                    frappe.msgprint("Commission Invoice generated & Submitted successfully")


    def generate_qrcode(self):
        doctype = self.doctype
        docname = self.name
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=10))
        res2 = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=6))
        filename = res+'-QRCode.png'.replace(os.path.sep, "__")

        qr_image = io.BytesIO()
        url = qrcreate(self.verification_url, error='L')
        url.png(qr_image, scale=3, quiet_zone=1)

        _file = frappe.get_doc({
            'doctype': 'File',
            'file_name': filename,
            'attached_to_doctype': doctype,
            'attached_to_name': docname,
            'attached_to_field': 'qrcode_path',
            'is_private': 0,
            'content': qr_image.getvalue()
        })
        _file.save()
        return _file.file_url

  

    def validate(self):
        dt = datetime.datetime.now()
        day = str(dt.day)
        month = str(dt.month)
        year = dt.strftime("%y")
        hr = str(dt.hour)
        min = str(dt.minute)
        id = day+"/"+month+"/"+year+"/"+hr+"/"+min 
        # frappe.msgprint(id)
        if self.status == "Batched":
            self.batch_id = "B-"+id

        if self.start_date and self.end_date:
            start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()
            p = end - start 
            self.period_of_issuance = p.days + 1

    
    
    def after_insert(self):
        
        
        # self.save()
        
        #Fetching data
        item = frappe.get_doc("Item", self.policy)
        # if self.start_date:
        #     self.period_of_issuance = item.period_of_issuance

        if self.policy:
            self.premium = item.standard_rate

        
        #Adding policy List Of Policy Doctype
        if self.endorsed==0:
            policy_list = frappe.get_list("List of Policy")
            if len(policy_list)==0:
                series_no = 0
            else:
                last_doc = frappe.get_last_doc("List of Policy")
                series_no = int(last_doc.series_number)+1
            list_of_policy = frappe.new_doc("List of Policy")
            list_of_policy.document = "Operator Policy Issued"
            list_of_policy.policy = self.policy_number
            list_of_policy.operator = self.operator
            list_of_policy.start_date = self.start_date
            list_of_policy.end_date = self.end_date
            list_of_policy.series_number = series_no
            list_of_policy.customer = self.name1
            list_of_policy.date_of_birth = self.dob
            list_of_policy.period_of_issuance = self.period_of_issuance 
            list_of_policy.amount = self.premium
            list_of_policy.policy_provider = self.policy_provider
            list_of_policy.date_of_issue = self.date_of_issue
            list_of_policy.insert()
