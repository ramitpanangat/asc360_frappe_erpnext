from . import __version__ as app_version

app_name = "a3_adventure_sports_cover"
app_title = "A3 Adventure Sports Cover"
app_publisher = "Ramit Panangat"
app_description = "Insurance for adventure sports."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ramit.panangat@acube.co"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/a3_adventure_sports_cover/css/a3_adventure_sports_cover.css"
# app_include_js = "/assets/a3_adventure_sports_cover/js/a3_adventure_sports_cover.js"

# include js, css files in header of web template
# web_include_css = "/assets/a3_adventure_sports_cover/css/a3_adventure_sports_cover.css"
# web_include_js = "/assets/a3_adventure_sports_cover/js/a3_adventure_sports_cover.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "a3_adventure_sports_cover/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }


website_route_rules = [
	{"from_route": "/view_invoice/<docname>", "to_route": "view_invoice"},
	{"from_route": "/view_issue_policy/<docname>", "to_route": "view_issue_policy"},
	{"from_route": "/view_issued_ticket/<docname>", "to_route": "view_issued_ticket"},
	{"from_route": "/view_payment/<docname>", "to_route": "view_payment"},
	{"from_route": "/view_activity/<docname>", "to_route": "view_activity"},
	{"from_route": "/view_equipment/<docname>", "to_route": "view_equipment"},
	{"from_route": "/view_ticket_master/<docname>", "to_route": "view_ticket_master"},
	{"from_route": "/view_payemnt/<docname>", "to_route": "view_ticket_master"},
	{"from_route": "/view_plan_master/<docname>", "to_route": "view_plan_master"},
	{"from_route": "/view_agent_commission/<docname>", "to_route": "view_agent_commission"},
	{"from_route": "/view_operator_commission/<docname>", "to_route": "view_operator_commission"},
	{"from_route": "/view_operator/<docname>", "to_route": "view_operator"},
	{"from_route": "/view_claims/<docname>", "to_route": "view_claims"},
]

# on_logout = "app.overide.clear_user_cache"


# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = [{"from_route": "/invoice/<docname>", "to_route":"/invoice"}]

# Installation
# ------------

# before_install = "a3_adventure_sports_cover.install.before_install"
# after_install = "a3_adventure_sports_cover.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "a3_adventure_sports_cover.uninstall.before_uninstall"
# after_uninstall = "a3_adventure_sports_cover.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "a3_adventure_sports_cover.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doctype_js = {
    "Contract": "custom_scripts/sales_invoice.js"
}

doc_events = {
 #	"*": {
 #		"on_update": "method",
 #		"on_cancel": "method",
 #		"on_trash": "method"
#	},
	'File': {
        "validate": "a3_adventure_sports_cover.a3_adventure_sports_cover.doc_events.files.validate"
  	},
	'Customer': {
        "validate": "a3_adventure_sports_cover.a3_adventure_sports_cover.doc_events.customer.validate"
  	},
	'Booking': {
        "on_submit": "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.booking.events.on_submit"
  	},
	'Union': {
      	"on_submit": "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.union.events.on_submit"
 	},
	# 'Operator': {
    #   	"on_submit": "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.operator.events.on_submit"
 	# },
	 'Operator Policy Issued': {
      	"after_insert": "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.operator_policy_issued.events.attach_pdf"
 	},
	 'Issue Policy': {
      	"after_insert": "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.issue_policy.events.attach_pdf"
 	},
	 'Sales Invoice': {
      	"on_submit": "a3_adventure_sports_cover.a3_adventure_sports_cover.doc_events.sales_invoice.on_submit"
 	},
	'Payment Entry': {
      	"on_submit": "a3_adventure_sports_cover.a3_adventure_sports_cover.doc_events.payment_entry.on_submit",
		"before_insert": "a3_adventure_sports_cover.a3_adventure_sports_cover.doc_events.payment_entry.before_insert"
 	}
 }

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"a3_adventure_sports_cover.tasks.all"
	# ],
	"cron": {
			"*/10 * * * *": [
				"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.create_single_policy",
				"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2c_policy_issue.events.create_single_b2c",
				"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2c_policy_issue.events.attach_pdf_cron_b2c",
				"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.attach_pdf_cron",
			],
			# "*/30 * * * *": [
			# 	"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.check_in_queue",
			# ],
	},
	# "hourly": [
	# 	"a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.create_operator_commission"
	# ],
	# "weekly": [
	# 	"a3_adventure_sports_cover.tasks.weekly"
	# ]
	# "monthly": [
	# 	"a3_adventure_sports_cover.policy_master.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "a3_adventure_sports_cover.install.before_tests"

fixtures = [{"dt":"Workspace"}, {"dt":"Print Format"}, {"dt":"Notification"}, {"dt":"Website Settings"}, {"dt":"Web Form"}, 
	{"dt":"Role", "filters": [
        [
            "name", "in", [
                "Policy Issuer"
            ]
        ]
    ]},
	{"dt":"Role Profile", "filters":[["name", "in", ["Operator Roles"]]]},
	{
		"dt": "Price List",
		"filters": [
			[
				"name", "in", [
					"USD Selling",
					"CNY Selling",
					"JPY Selling"
				]
			]
		]
	}
	]

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "a3_adventure_sports_cover.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "a3_adventure_sports_cover.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"a3_adventure_sports_cover.auth.validate"
# ]

