import frappe
from frappe import get_doc, publish_progress, _, get_single, new_doc, get_list, get_value
from frappe.core.doctype.file.file import create_new_folder
from a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events import send_whatsapp_notification
from frappe.utils.file_manager import save_file
from datetime import datetime
import requests


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


######################################## Frappe Call Functions ###########################################
@frappe.whitelist()
def get_customer_data(customer):
    customer = get_value("Customer", customer, "customer_primary_address")
    if frappe.db.exists("Address", customer):
        address = get_doc("Address", customer)
        return address.as_dict()
    else:
        return "No address found"


######################################## Create Single Policy Cron Job ###########################################
def create_single_b2c():
    queue_doc = get_single("B2C Policy Queue")
    batch_count = 0
    while batch_count <= queue_doc.no_of_batches:
        for policy in queue_doc.policy_list:
            if policy.priority_ranking == batch_count:
                customer_name = policy.customer_name
                date_of_birth = policy.date_of_birth
                if isinstance(date_of_birth, str):
                    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

                if not frappe.db.exists("Customer", {"customer_name":customer_name,"email_id":policy.email_id, "mobile_no":policy.contact}):
                    customer = new_doc("Customer")
                    customer.customer_name = customer_name
                    customer.customer_group = "Individual"
                    customer.customer_type = "Individual"
                    customer.date_of_birth = date_of_birth
                    customer.territory = "India"
                    customer.gender = policy.gender
                    customer.aadhaar_card = policy.aadhar_number
                    customer.pan = policy.pan_number
                    customer.passport_number = policy.passport_number
                    customer.insert()

                    contact = new_doc("Contact")
                    contact.first_name = customer_name
                    contact.gender = policy.gender
                    contact.append("email_ids", {
                        "email_id": policy.email_id,
                        "is_primary": 1
                    })
                    contact.append("phone_nos", {
                        "phone": policy.contact,
                        "is_primary_phone": 1,
                        "is_primary_mobile_no": 1
                    })
                    contact.append("links", {
                        "link_doctype": "Customer",
                        "link_name": customer.name,
                        "link_title": customer.name
                    })
                    contact.insert()
                    customer.customer_primary_contact = contact.name

                    if policy.address and policy.city_town:
                        address = new_doc("Address")
                        address.address_title = customer_name
                        address.address_line1 = policy.address
                        address.address_line2 = policy.address_line_2
                        address.city = policy.city_town
                        address.state = policy.state
                        address.country = policy.country
                        address.pincode = policy.pincode
                        address.append("links", {
                            "link_doctype": "Customer",
                            "link_name": customer.name,
                            "link_title": customer.name
                        })
                        address.insert()
                        customer.customer_primary_address = address.name
                    customer.save()
                    customer_name = customer.name
                else:
                    customer_name = get_doc("Customer", {"customer_name":customer_name,"email_id":policy.email_id, "mobile_no":policy.contact})

                bulk_doc = get_doc("B2C Policy Issue", policy.main_policy)
                single_doc = new_doc("B2C Policy Issue")
                single_doc.policy_type = "Single Policy"
                single_doc.batch_id = bulk_doc.name
                single_doc.invoice_and_payment = bulk_doc.invoice_and_payment
                single_doc.admin_approved = policy.admin_approved
                single_doc.mode_of_payment = bulk_doc.mode_of_payment
                single_doc.reference_no = bulk_doc.reference_no
                single_doc.payment_id = bulk_doc.payment_id
                single_doc.paid_amount = bulk_doc.paid_amount
                single_doc.account_paid_to = bulk_doc.account_paid_to
                single_doc.reference_date = bulk_doc.reference_date
                single_doc.invoice_number = bulk_doc.invoice_number
                single_doc.start_date = bulk_doc.start_date
                single_doc.end_date = bulk_doc.end_date
                single_doc.policy_name = bulk_doc.policy_name
                single_doc.start_location = bulk_doc.start_location
                single_doc.amount = bulk_doc.amount
                single_doc.policy_provider = bulk_doc.policy_provider
                single_doc.tour_operator_name = bulk_doc.tour_operator_name
                single_doc.policy = bulk_doc.policy
                single_doc.end_location = bulk_doc.end_location
                single_doc.period_of_issuance = bulk_doc.period_of_issuance
                single_doc.trip_type = bulk_doc.trip_type
                single_doc.tour_package_name = bulk_doc.tour_package_name
                single_doc.send_whatsapp_alert = bulk_doc.send_whatsapp_alert
                single_doc.send_sms_alert = bulk_doc.send_sms_alert
                single_doc.customer_name = customer_name
                single_doc.gender = policy.gender
                single_doc.email_id = policy.email_id
                single_doc.date_of_birth = policy.date_of_birth
                single_doc.nationality = policy.nationality
                single_doc.phone_number = policy.contact
                single_doc.address_line_1 = policy.address
                single_doc.address_line_2 = policy.address_line_2
                single_doc.citytown = policy.city_town
                single_doc.state_ut = policy.state
                single_doc.country = policy.country
                single_doc.pin_code = policy.pincode
                single_doc.event = policy.event
                single_doc.nomine_name = policy.nominee_name
                single_doc.nominee_relationship = policy.nominee_relationship
                single_doc.nominee_contact = policy.nominee_contact
                single_doc.save()
                single_doc.submit()
                queue_doc.policy_list.remove(policy)
        queue_doc.save()
        batch_count += 1

######################################## Attach PDf ###########################################

def attach_pdf_cron_b2c():
    single_docs = get_list("B2C Policy Issue", filters={"policy_type":"Single Policy", "docstatus": 1, "policy_status": "In Process"})
    for docs in single_docs:
        policy = get_doc("B2C Policy Issue", docs.name)
        attach_pdf(policy)

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
    document = get_doc(doc.doctype, doc.name)
    document.policy_status = "Completed"
    if document.batch_id:
        batch = get_doc(doc.doctype, document.batch_id)
        batch.append("policy_generated_list", {
            "customer_name": document.customer_name,
            "policy_number": document.name,
            "pdf_added": "Yes"
        })
        batch.save()
        batch.db_update()
    document.save()
    document.db_update()
    send_sms_notification(document)
    send_whatsapp_notification(document, "Submit")

def send_sms_notification(doc):
    sms_config = frappe.get_single("SMS Configuration")
    if sms_config.b2c_enable == 1:
        if doc.send_sms_alert == "Yes":
            date_of_issue = doc.date_of_issuance
            if isinstance(date_of_issue, str):
                date_of_issue = datetime.strptime(date_of_issue, "%Y-%m-%d").date()
            date_of_issue = date_of_issue.strftime("%d-%m-%Y")
            phone_number = doc.phone_number[2:]
            re = requests.get(f"{sms_config.api_url}?authorization={sms_config.api_key}&route=dlt&sender_id={sms_config.sender_id}&message=135060&variables_values={date_of_issue}%7C{doc.name}%7C&flash=0&numbers={phone_number}")
            response = re.json()
            sms_log = frappe.new_doc("SMS Notification Log")
            sms_log.document_type = "B2C Policy Issue"
            sms_log.document = doc.name
            sms_log.status = "Success" if response["return"] else "Failed"
            sms_log.result = f"{response}\nPhone:{phone_number}"
            sms_log.insert()

def enqueue(args):
    """Add method `execute` with given args to the queue."""
    frappe.enqueue(method=execute, queue='long',
                   timeout=3000, is_async=False, **args)


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