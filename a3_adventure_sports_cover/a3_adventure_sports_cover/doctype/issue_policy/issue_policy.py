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
from re import search, findall


class IssuePolicy(Document):
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
    #         )
    #     else:
    #         self.S3_CLIENT = boto3.client('s3')
    #     self.BUCKET = self.s3_settings_doc.bucket_name
    #     self.folder_name = self.s3_settings_doc.folder_name

    def before_insert(self):
        pass
        # res = ''.join(random.choices(string.ascii_uppercase +
        #                              string.digits, k=17))
        # s3_key_name_hash = hashlib.sha256(str(self.name).encode() + str(res).encode())

        # if not s3_key_name_hash:
        #     frappe.throw("Unable to Create s3 name")

        # s3_file_name = datetime.now().strftime('%h-%Y').lower() + "-" + s3_key_name_hash.hexdigest()
        # self.unique_hash        = str(s3_file_name)
        # self.verification_url   = "https://verify.djiboutiimmigration.com?id="+s3_file_name
        # self.qrcode_path        = self.generate_qrcode()

    def on_submit(self):
        if self.operator_commission_received:
            commission = self.operator_commission_received
        if self.operator:
            operator = frappe.get_doc("Operator",self.operator)
            partner = operator.sales_partner_id
        if(self.grand_total):
            invoice = frappe.new_doc("Sales Invoice")
            invoice.customer = self.customer
            invoice.due_date = self.date_of_issue
            invoice.discount_amount = self.discount
            invoice.operator = self.operator
            invoice.sales_partner = self.operator
            invoice.commission_rate = self.operator_commission_percentage
            invoice.total_commission = commission
            invoice.append(
                "items",
                {
                    "item_code": self.policy,
                    "qty": self.quantity,
                    "rate": self.rate
                },
            )
            invoice.set_missing_values()
            invoice.insert()
            invoice.submit()

            frappe.msgprint("Sales Invoice generated & Submitted successfully")

        else:
            frappe.msgprint("Submitted without invoice creation as amount not found!!")

        # values = {
        #     "name": self.name,
        #     "operator": self.operator,
        #     "customer": self.customer,
        #     "policy": self.policy,
        #     "supplier": self.supplier,
        #     "date_of_issue": self.date_of_issue,
        #     "date_of_birth": self.date_of_birth,
        #     "start_date": self.beginning_date,
        #     "end_date": self.end_date,
        #     "period_of_issuance": self.period_of_issuance,
        # }





        if frappe.db.exists("Commission Report", self.operator):
            commission_doc = frappe.get_doc("Commission Report", self.operator)
            commission_doc.operator = self.operator
            commission_doc.append("commission_report",{
                "operator" :self.operator,
                "customer": self.customer,
                "issue_policy": self.name,
                "date_of_issue": self.date_of_birth,
                "supplier": self.supplier,
                "policy": self.policy,
                "quantity": self.quantity,
                "policy_rate": self.rate,
                "operator_commission_receivable": self.operator_commission_received,
                "grand_total": self.grand_total
                })
            commission_doc.save()
        else:
            commission_doc = frappe.new_doc("Commission Report")
            commission_doc.operator = self.operator
            commission_doc.append("commission_report",{
                "operator" :self.operator,
                "customer": self.customer,
                "issue_policy": self.name,
                "date_of_issue": self.date_of_birth,
                "supplier": self.supplier,
                "policy": self.policy,
                "quantity": self.quantity,
                "policy_rate": self.rate,
                "operator_commission_receivable": self.operator_commission_received,
                "grand_total": self.grand_total
                })
            commission_doc.insert()


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
        message_rule = frappe.get_doc("WhatsApp Message Rule", {"document_type": "B2B Policy Issue", "alert_for": "Submit"})
        parameters = []
        for params in message_rule.parameter_mapping:
            name = findall(r"\(([A-Za-z0-9_]+)\)", params.value)
            parameter = {
                "name": params.parameter,
                "value": name
            }
            parameters.append(parameter)
        print(parameters)

        if self.policy:
            item = frappe.get_doc('Item',self.policy)
            for item in item.benefit_details:
                for row in self.plan_details:
                    row.benefits = item.benefit
                    row.sum_insured = item.amount
                    row.deductible = item.deductible

        if self.operator:
            operator = frappe.get_doc("Operator",self.operator)
            partner = operator.sales_partner_id
            frappe.msgprint(partner)

        if self.operator:
            territory_code = self.territory_code
            scope = self.scope_of_policy
            type = self.type_of_policy
            op_code = self.operator_code
            if scope == "International":
                scope = "I"
            elif scope == "Domestic":
                scope = "D"
            if type == "Short Term":
                type = "S"
            elif type == "Annual":
                type = "A"
            policy_code = f"{territory_code}{scope}{type}{op_code}"
            self.issue_code = policy_code

        if self.beginning_date:
            item = frappe.get_doc("Item", self.policy)
            self.period_of_issuance = item.period_of_issuance
            # self.end_date = frappe.utils.add_days(self.beginning_date, int(self.period_of_issuance))

        if self.policy:
            rate = float(self.rate)
            qty = float(self.quantity)
            amount = rate*qty
            self.amount = amount
            if self.customer_discount_type == "Amount":
                discount = float(self.customer_discount_amount)
                total_discount = discount * qty
                if self.amount< total_discount:
                    self.grand_total = amount
                else:
                    # total_discount = discount * qty
                    self.discount = total_discount
                    total = amount - total_discount
                    self.grand_total = total

            elif self.customer_discount_type == "Percentage":
                disc_percentage = float(self.customer_discount_percentage)
                discount_amt = amount * (disc_percentage/100)
                # total_discount = discount_amt * qty
                self.discount = discount_amt
                total = amount - discount_amt
                self.grand_total = total

            else:
                self.grand_total = amount

            if self.master_policy:
                qty = float(self.quantity)
                master_policy = frappe.get_doc("Policy Master",self.master_policy)
                master_comm_type = master_policy.policy_commission_type
                if master_policy:
                    if master_comm_type == "Percentage":
                        master_percentage = float(master_policy.commission_percentage)
                        m_total = float(self.grand_total)
                        m_amt = (m_total * (master_percentage/100)) * qty
                    elif master_comm_type == "Amount":
                        master_amount = float(master_policy.commission_amount)

            # if self.operator:
            #     if self.operator_commission_type == "Amount":
            #         comm_amt = float(self.operator_commission_amount)
            #         if self.master_policy:
            #             if master_comm_type == "Amount":
            #                 if master_amount<comm_amt:

            #                     comm_amt = master_amount
            #                     total_comm = comm_amt * qty
            #                     self.operator_commission_received = total_comm
            #             else:
            #                 total_comm = comm_amt * qty
            #                 self.operator_commission_received = total_comm

            #     elif self.operator_commission_type == "Percentage":
            #         comm_percentage = float(self.operator_commission_percentage)
            #         if self.master_policy:
            #             if master_comm_type == "Percentage":
            #                 master_percentage = float(master_policy.commission_percentage)
            #                 if master_percentage<comm_percentage:
            #                     comm_percentage = master_percentage
            #                     total = float(self.grand_total)
            #                     commission = (total * (comm_percentage/100))
            #                     self.operator_commission_received = commission
            #                 else:
            #                     commission = 100
            #             else:
            #                 comm_percentage = float(self.operator_commission_percentage)
            #                 total = float(self.grand_total)
            #                 commission = (total * (comm_percentage/100))
            #                 self.operator_commission_received = commission
            #         else:
            #             comm_percentage = float(self.operator_commission_percentage)
            #             total = float(self.grand_total)
            #             commission = (total * (comm_percentage/100))
            #             self.operator_commission_received = commission
