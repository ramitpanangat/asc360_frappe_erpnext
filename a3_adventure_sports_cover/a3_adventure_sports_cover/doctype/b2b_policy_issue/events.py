from dataclasses import fields
from email import policy
from pydoc import doc
from warnings import filters
import frappe
from frappe import get_doc, get_list, get_single, new_doc, publish_progress, _
from frappe.core.doctype.file.file import create_new_folder
from frappe.utils.file_manager import save_file
from datetime import datetime
import requests
from re import findall
from json import dumps
################### Check if policy entered in the queue ###################

@frappe.whitelist()
def check_in_queue():
	b2b_list = get_list("B2B Policy Issue", filters={"policy_type":"Bulk Policy", "docstatus":1, "pdf_added":"In Process"})
	b2b_queue = get_single("B2B Policy Queue")
	for b2b in b2b_list:
		b2b_doc = get_doc("B2B Policy Issue", b2b.name)
		for policy in b2b_doc.bulk_upload:
			customer_name = str(policy.name1).strip()
			if not frappe.db.exists("B2B Policy Issue", {"customer_name":customer_name, "batch_id":b2b_doc.name}):
				has_in_queue = False
				for customer in b2b_queue.customer_details:
					if customer.customer_name == customer_name and customer.main_policy == b2b_doc.name:
						has_in_queue = True
				if not has_in_queue:
					b2b_queue.append("customer_details", {
						"priority_ranking": b2b_queue.no_of_policies + 1,
						"main_policy": b2b_doc.name,
						"customer_name": customer_name,
						"gender": policy.gender,
						"date_of_birth": policy.date_of_birth,
						"email_id": policy.email_id,
						"contact": policy.contact,
						"address": policy.address,
						"event": policy.event,
						"pan_number": policy.pan_number,
						"aadhar_number": policy.aadhar_number,
						"passport_number": policy.passport_number,
						"nominee_name": policy.nominee_name,
						"nominee_contact": policy.nominee_contact,
						"nominee_relationship": policy.nominee_relationship,
						"admin_approved": b2b_doc.admin_approved
					})
		b2b_queue.no_of_policies += 1
		b2b_queue.save()
		

################### Cancel Document ###################
@frappe.whitelist()
def cancel_document(document, batch_id=""):
	current_time = datetime.now()
	customer = ""
	b2b = frappe.get_doc("B2B Policy Issue", document)
	if b2b.policy_type == "Single Policy":
		if batch_id != "":
			batch_policy = frappe.get_doc("B2B Policy Issue", batch_id)
			for policy in batch_policy.policy_list:
				if policy.policy == document:
					batch_policy.policy_list.remove(policy)
					customer = policy.customer

			batch_policy.append("policy_cancelled", {
				"policy_number":document,
				"customer_name": customer,
				"cancelled_on": current_time,
				"cancelled_by": frappe.session.user
			})
			batch_policy.save()
			batch_policy.db_update()

	b2b.cancel()

	if frappe.db.exists("List of Policy", document):
		lop = frappe.get_doc("List of Policy", document)
		lop.policy_status = "Cancelled"
		lop.policy = ""
		lop.save()

	if frappe.db.exists("Operator Commission Payable", {"policy_number":document}):
		comm = frappe.get_doc("Operator Commission Payable", {"policy_number":document})
		comm.status = "Cancelled"
		comm.policy_number = ""
		comm.policy_id = f"{document}"
		comm.save()
	
	if frappe.db.exists("Sales Invoice", {"policy_number": document}):
		invoice = frappe.get_doc("Sales Invoice", {"policy_number": document})
		invoice.cancel()
	
	if frappe.db.exists("Payment Entry", {"policy_number": document}):
		payment = frappe.get_doc("Payment Entry", {"policy_number": document})
		payment.cancel()

	return "Document cancelled successfully."


################### Cancel Document from Listview ###################
@frappe.whitelist()
def cancel_checked(**kwargs):
	del kwargs['cmd']
	for item in kwargs:
		cancel_doc = frappe.get_doc("B2B Policy Issue", kwargs[item])
		current_time = datetime.now()
		if cancel_doc.batch_id:
			bulk_doc = frappe.get_doc("B2B Policy Issue", cancel_doc.batch_id)
			customer = ""
			for policy in bulk_doc.policy_list:
				if policy.policy == cancel_doc.name:
					bulk_doc.policy_list.remove(policy)
					customer = policy.customer

			bulk_doc.append("policy_cancelled", {
				"policy_number":cancel_doc.name,
				"customer_name": customer,
				"cancelled_on": current_time,
				"cancelled_by": frappe.session.user
			})
			bulk_doc.save()
			bulk_doc.db_update()

			if frappe.db.exists("List of Policy", cancel_doc.name):
				lop = frappe.get_doc("List of Policy", cancel_doc.name)
				lop.policy_status = "Cancelled"
				lop.policy = ""
				lop.save()

			if frappe.db.exists("Operator Commission Payable", {"policy_number":cancel_doc.name}):
				comm = frappe.get_doc("Operator Commission Payable", {"policy_number":cancel_doc.name})
				comm.status = "Cancelled"
				comm.policy_id = f"{cancel_doc.name}"
				comm.policy = ""
				comm.save()
			
			if frappe.db.exists("Sales Invoice", {"policy_number": cancel_doc.name}):
				invoice = frappe.get_doc("Sales Invoice", {"policy_number": cancel_doc.name})
				print(invoice)
				invoice.cancel()
			
			if frappe.db.exists("Payment Entry", {"policy_number": cancel_doc.name}):
				payment = frappe.get_doc("Payment Entry", {"policy_number": cancel_doc.name})
				payment.cancel()
		cancel_doc.cancel()



################### Download Document PDF ###################
@frappe.whitelist()
def download_pdf(**kwargs):
	file_urls = {}
	files_index = 0
	site = frappe.local.request.host  # site name fetched dynamically
	del kwargs["cmd"] # remove cmd key-value from the dictionary

	# loop through all the checked items and create a link and append it to file_url dictionary
	for item in kwargs:
		file_url = f"https://{site}/files/{kwargs[item]}.pdf"
		file_urls[files_index] = file_url
		files_index += 1
	return file_urls


################### Download Document PDF from bulk policy page ###################
@frappe.whitelist()
def bulk_download(**kwargs):
	del kwargs["cmd"]
	print(kwargs)
	file_urls = {}
	file_index = 0
	site = frappe.local.request.host
	bulk_doc = get_doc("B2B Policy Issue", kwargs["doc"])
	for doc in bulk_doc.policy_list:
		for row in kwargs:
			if row != "doc":
				if kwargs[row] == doc.name:
					file_url = f"https://{site}/files/{doc.policy}.pdf"
					file_urls[file_index] = file_url
					file_index +=1
	return file_urls



################### Get list of Customised Policy ###################
@frappe.whitelist()
def get_customised_policy(operator=None):
	product_mapping = frappe.get_all("Operator Product Mapping", filters={"operator": operator}, fields=["policy"])
	return product_mapping



################### Create Single Policy from Bulk Policy ###################
def create_single_policy():
	queue_doc = get_single("B2B Policy Queue")
	batch_count = 0
	while batch_count <= queue_doc.no_of_policies:
		for customer in queue_doc.customer_details:
			if customer.priority_ranking == batch_count:
				customer_name = str(customer.customer_name).strip()

				#################### Check customer existence and create if not exist ####################
				date_of_birth = customer.date_of_birth
				if isinstance(date_of_birth, str):
					date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")

				if not frappe.db.exists("Customer", {"customer_name":customer_name, "email_id": customer.email_id, "mobile_no":customer.contact, "date_of_birth":date_of_birth}):
					customer_doc = frappe.new_doc("Customer")
					customer_doc.customer_name = customer_name
					customer_doc.customer_type = "Individual"
					customer_doc.customer_group = "All Customer Groups"
					customer_doc.gender = customer.gender
					customer_doc.territory = "India"
					customer_doc.date_of_birth = date_of_birth
					customer_doc.insert()

					contact = frappe.new_doc("Contact")
					contact.first_name = customer_name
					contact.email_id = customer.email_id
					contact.gender = customer.gender
					contact.append("email_ids", {
						"email_id": customer.email_id,
						"is_primary": 1
					})
					contact.append("phone_nos", {
						"phone": customer.contact,
						"is_primary_phone": 1,
						"is_primary_mobile_no": 1
					})
					contact.append("links", {
						"link_doctype": "Customer",
						"link_name": customer_doc.name,
						"link_title": customer_doc.name
					})
					contact.insert()
					customer_doc.customer_primary_contact = contact.name
					customer_doc.mobile_no = customer.contact
					customer_doc.email_id = customer.email_id
					customer_doc.save()
					customer_name = customer_doc.name
				else:
					customer_name = frappe.get_doc("Customer", {"customer_name":customer_name, "email_id": customer.email_id, "mobile_no":customer.contact, "date_of_birth":date_of_birth}).name

				#################### B2B Policy creation ####################
				if not frappe.db.exists("B2B Policy Issue", {"batch_id": customer.main_policy, "customer_name": customer_name, "email_id" : customer.email_id}):
					bulk_doc = get_doc("B2B Policy Issue", customer.main_policy)
					single_doc = new_doc("B2B Policy Issue")
					single_doc.policy_issued_by = bulk_doc.policy_issued_by
					single_doc.admin_approved = customer.admin_approved
					if bulk_doc.policy_issued_by == "Operator":
						op = frappe.get_value("Operator", bulk_doc.operator, "email")
						op_bal = frappe.get_value("Operator Balance", bulk_doc.operator, "balance_available")
						if bulk_doc.operator_email_preference:
							single_doc.operator_email_preference = bulk_doc.operator_email_preference
						single_doc.operator = bulk_doc.operator
						single_doc.operator_balance = op_bal
						single_doc.operator_email = bulk_doc.operator_email
					elif bulk_doc.policy_issued_by == "Agent":
						op = frappe.get_value("Agent", bulk_doc.agent_name, "agent_email")
						single_doc.agent_name = bulk_doc.operator
						single_doc.agent_email = bulk_doc.agent_email
					single_doc.policy_type = "Single Policy"
					single_doc.start_date = bulk_doc.start_date
					single_doc.end_date = bulk_doc.end_date
					single_doc.policy_name = bulk_doc.policy_name
					single_doc.policy = bulk_doc.policy
					single_doc.amount = bulk_doc.amount
					single_doc.policy_provider = bulk_doc.policy_provider
					single_doc.send_whatsapp_alert = bulk_doc.send_whatsapp_alert
					single_doc.send_sms_alert = bulk_doc.send_sms_alert
					single_doc.customer_name = customer_name
					single_doc.gender = customer.gender
					single_doc.date_of_birth = customer.date_of_birth
					single_doc.email_id = customer.email_id
					single_doc.phone_number = customer.contact
					single_doc.address = customer.address
					single_doc.nationality = customer.nationality
					single_doc.event = customer.event
					single_doc.nominee_name = customer.nominee_name
					single_doc.nominee_contact_number = customer.nominee_contact
					single_doc.nominee_relationship = customer.nominee_relationship
					single_doc.start_location = bulk_doc.start_location
					single_doc.end_location = bulk_doc.end_location
					single_doc.batch_id = bulk_doc.bulk_policy_number 
					single_doc.status = "Issued"
					if customer.pan_number:
						single_doc.append("customer_documents",{
								"document_name" : "PAN",
								"document_number" : customer.pan_number
						})
					if customer.aadhar_number:
						single_doc.append("customer_documents",{
								"document_name" : "Aadhar",
								"document_number" : customer.aadhar_number
						})
					if customer.passport_number:
						single_doc.append("customer_documents",{
								"document_name" : "Passport",
								"document_number" : customer.passport_number
						})
					single_doc.save()
					single_doc.submit()
					queue_doc.customer_details.remove(customer)
				else:
					queue_doc.customer_details.remove(customer)
			
		queue_doc.save()
		batch_count += 1


################### Add to Queue ###################

@frappe.whitelist()
def add_to_queue(batch):
	bulk = frappe.get_doc("B2B Policy Issue", batch)
	queue_doc = frappe.get_single("B2B Policy Queue")
	for policy in bulk.bulk_upload:
		if not frappe.db.exists("B2B Policy Issue", {"policy_type": "Single Policy", "customer_name": policy.name1, "batch_id": bulk.name}):
			has_already = False
			if len(queue_doc.customer_details)>0:
				for detail in queue_doc.customer_details:
					if detail.main_policy == bulk.name and detail.customer_name == policy.name1 and detail.date_of_birth == policy.date_of_birth:
						has_already = True

			if not has_already:
				queue_doc.append("customer_details",
				{
					"priority_ranking": queue_doc.no_of_policies + 1,
					"main_policy": bulk.name,
					"customer_name": str(policy.name1).strip(),
					"gender": policy.gender,
					"date_of_birth": policy.date_of_birth,
					"email_id": policy.email_id,
					"contact": policy.contact,
					"address": policy.address,
					"event": policy.event,
					"pan_number": policy.pan_number,
					"aadhar_number": policy.aadhar_number,
					"passport_number": policy.passport_number,
					"nominee_name": policy.nominee_name,
					"nominee_contact": policy.nominee_contact,
					"nominee_relationship": policy.nominee_relationship,
					"admin_approved": bulk.admin_approved
				})
	queue_doc.save()
	return "All policies are successfully added to queue."



################### Attach PDF to all Single Policy ###################
def attach_pdf_cron():
	all_b2b = get_list("B2B Policy Issue", filters={"pdf_added":"In Process", "policy_type": "Single Policy", "docstatus":1})
	for b2b in all_b2b:
		b2b_doc = get_doc("B2B Policy Issue", b2b.name)
		attach_pdf(b2b_doc)


def attach_pdf(doc, event=None):
	fallback_language = frappe.db.get_single_value("System Settings", "language") or "en"
	args = {
		"doctype": doc.doctype,
		"name": doc.name,
		"title": doc.get_title(),
		"lang": getattr(doc, "language", fallback_language),
		"show_progress": 0
	}
	execute(**args)
	document = frappe.get_doc(doc.doctype, doc.name)
	document.pdf_added = "Completed"
	# send_whatsapp_notification(doc=document, alert_on="Submit")
	send_sms_notification(doc=document)
	if document.batch_id:
		bulk_doc = frappe.get_doc(doc.doctype, document.batch_id)
		bulk_doc.append("policy_list", {
					"customer": document.customer_name,
					"policy": document.name,
					"pdf_added": "Yes"
				})
		bulk_doc.save()
		bulk_doc.db_update()
	document.save()
	document.db_update()

def enqueue(args):
	"""Add method `execute` with given args to the queue."""
	frappe.enqueue(method=execute, queue='long', is_async=False, timeout=3000, **args)
	
def execute(doctype, name, title, lang=None, show_progress=True):
	"""
	Queue calls this method, when it's ready.
	1. Create necessary folders
	2. Get raw PDF data
	3. Save PDF file and attach it to the document
	"""
	progress = frappe._dict(title=_("Creating PDF ..."), percent=0, doctype=doctype, docname=name)

	if lang:
		frappe.local.lang = lang

	if show_progress:
		publish_progress(**progress)

	doctype_folder = create_folder(_(doctype), "Home")
	title_folder = create_folder(title, doctype_folder)

	if show_progress:
		progress.percent = 33
		publish_progress(**progress)

	pdf_data = get_pdf_data(doctype, name)

	if show_progress:
		progress.percent = 66
		publish_progress(**progress)

	fileurl = save_and_attach(pdf_data, doctype, name, title_folder)

	if show_progress:
		progress.percent = 100
		publish_progress(**progress)


def create_folder(folder, parent):
	"""Make sure the folder exists and return it's name."""
	new_folder_name = "/".join([parent, folder])

	if not frappe.db.exists("File", new_folder_name):
		create_new_folder(folder, parent)

	return new_folder_name


def get_pdf_data(doctype, name):
	"""Document -> HTML -> PDF."""
	html = frappe.get_print(doctype, name)
	return frappe.utils.pdf.get_pdf(html)


def save_and_attach(content, to_doctype, to_name, folder):
	"""
	Save content to disk and create a File document.
	File document is linked to another document.
	"""
	file_name = "{}.pdf".format(to_name.replace(" ", "-").replace("/", "-"))
	fileName = save_file(file_name, content, to_doctype,
			  to_name, folder=folder, is_private=0)



def send_sms_notification(doc):
	sms_config = frappe.get_single("SMS Configuration")
	if sms_config.b2b_enable == 1:
		if doc.send_sms_alert == "Yes":
			date_of_issue = doc.date_of_issue
			if isinstance(date_of_issue, str):
				date_of_issue = datetime.strptime(date_of_issue, "%Y-%m-%d").date()
			date_of_issue = date_of_issue.strftime("%d-%m-%Y")
			phone_number = doc.phone_number[2:]
			re = requests.get(f"{sms_config.api_url}?authorization={sms_config.api_key}&route=dlt&sender_id={sms_config.sender_id}&message=135060&variables_values={date_of_issue}%7C{doc.name}%7C&flash=0&numbers={phone_number}")
			response = re.json()
			sms_log = frappe.new_doc("SMS Notification Log")
			sms_log.document_type = "B2B Policy Issue"
			sms_log.document = doc.name
			sms_log.status = "Success" if response["return"] else "Failed"
			sms_log.result = f"{response}\nPhone:{phone_number}"
			sms_log.insert()

def send_whatsapp_notification(doc, alert_on):
	if frappe.db.exists("WhatsApp Message Rule", {"document_type": doc.doctype, "alert_for": alert_on}):
		if doc.send_whatsapp_alert == "Yes":
			whatsapp_config = frappe.get_single("WhatsApp Configuration")
			message_rule = frappe.get_doc("WhatsApp Message Rule", {"document_type": doc.doctype, "alert_for": alert_on})
			doc_data = doc.as_dict()
			url = f"{whatsapp_config.api_url}?whatsappNumber={doc.phone_number}"
			parameters = []
			for params in message_rule.parameter_mapping:
				name = findall(r"\(([A-Za-z0-9_]+)\)", str(params.value))[0]
				data = doc_data[name]
				if name=="start_date" or name=="end_date":
					if isinstance(data, str):
						data = datetime.strptime(data, "%Y-%m-%d")
						data = data.strftime("%d-%m-%Y")
					else:
						data = data.strftime("%d-%m-%Y")
				parameter = {
					"name": params.parameter,
					"value": data
				}
				parameters.append(parameter)
			headers = {
				"content-type": "text/json",
				"Authorization": whatsapp_config.api_token
			}
			payload = {
				"parameters": parameters,
				"broadcast_name": message_rule.template,
				"template_name": message_rule.template
			}
			re = requests.post(url, json=payload, headers=headers)
			response = re.json()
			log = frappe.new_doc("WhatsApp Log")
			log.result = f"{response}"
			log.parameters = f"{parameters}"
			log.status = "Success" if response["result"] else "Failed"
			log.notification_type = alert_on
			log.document = doc.name
			log.document_type = doc.doctype
			log.insert()

