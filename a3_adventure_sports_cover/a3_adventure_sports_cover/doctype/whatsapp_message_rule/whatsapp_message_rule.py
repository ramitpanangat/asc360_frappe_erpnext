# Copyright (c) 2022, Ramit Panangat and contributors
# For license information, please see license.txt

from frappe import db, throw
from frappe.model.document import Document
from re import findall

class WhatsAppMessageRule(Document):
	def before_insert(self):
		if db.exists("WhatsApp Message Rule", {"document_type": self.document_type, "alert_for": self.alert_for}):
			throw(f"{self.alert_for} notification for document {self.document_type} already exists.")