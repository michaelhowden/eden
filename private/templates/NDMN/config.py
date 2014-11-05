# -*- coding: utf-8 -*-

try:
    # Python 2.7
    from collections import OrderedDict
except:
    # Python 2.6
    from gluon.contrib.simplejson.ordered_dict import OrderedDict

from gluon import current
from gluon.storage import Storage
from gluon.validators import IS_NOT_EMPTY

from s3.s3forms import S3SQLCustomForm

T = current.T
settings = current.deployment_settings

"""
    Template settings

    All settings which are to configure a specific template are located here

    Deployers should ideally not need to edit any other files outside of their template folder
"""

settings.base.system_name = T("Sahana - National Donation Management Network DEMO")
settings.base.system_name_short = T("Sahana")

# PrePopulate data
settings.base.prepopulate = ("NDMN",)

# Theme (folder to use for views/layout.html)
settings.base.theme = "NDMN"

settings.ui.formstyle_row = "bootstrap"
settings.ui.formstyle = "bootstrap"
settings.ui.filter_formstyle = "bootstrap"

# Authentication settings
# Should users be allowed to register themselves?
#settings.security.self_registration = False
# Do new users need to verify their email address?
#settings.auth.registration_requires_verification = True
# Do new users need to be approved by an administrator prior to being able to login?
#settings.auth.registration_requires_approval = True
#settings.auth.registration_requests_organisation = True

# Approval emails get sent to all admins
settings.mail.approver = "ADMIN"

# Restrict the Location Selector to just certain countries
# NB This can also be over-ridden for specific contexts later
# e.g. Activities filtered to those of parent Project
settings.gis.countries = ("US",)

# L10n settings
# Languages used in the deployment (used for Language Toolbar & GIS Locations)
# http://www.loc.gov/standards/iso639-2/php/code_list.php
#settings.L10n.languages = OrderedDict([
#    ("ar", "العربية"),
#    ("bs", "Bosanski"),
#    ("en", "English"),
#    ("fr", "Français"),
#    ("de", "Deutsch"),
#    ("el", "ελληνικά"),
#    ("es", "Español"),
#    ("it", "Italiano"),
#    ("ja", "日本語"),
#    ("km", "ភាសាខ្មែរ"),
#    ("ko", "한국어"),
#    ("ne", "नेपाली"),          # Nepali
#    ("prs", "دری"), # Dari
#    ("ps", "پښتو"), # Pashto
#    ("pt", "Português"),
#    ("pt-br", "Português (Brasil)"),
#    ("ru", "русский"),
#    ("tet", "Tetum"),
#    ("tl", "Tagalog"),
#    ("ur", "اردو"),
#    ("vi", "Tiếng Việt"),
#    ("zh-cn", "中文 (简体)"),
#    ("zh-tw", "中文 (繁體)"),
#])
# Default language for Language Toolbar (& GIS Locations in future)
#settings.L10n.default_language = "en"
# Uncomment to Hide the language toolbar
#settings.L10n.display_toolbar = False
# Default timezone for users
#settings.L10n.utc_offset = "UTC +0100"

# Security Policy
# http://eden.sahanafoundation.org/wiki/S3AAA#System-widePolicy
# 1: Simple (default): Global as Reader, Authenticated as Editor
# 2: Editor role required for Update/Delete, unless record owned by session
# 3: Apply Controller ACLs
# 4: Apply both Controller & Function ACLs
# 5: Apply Controller, Function & Table ACLs
# 6: Apply Controller, Function, Table ACLs and Entity Realm
# 7: Apply Controller, Function, Table ACLs and Entity Realm + Hierarchy
# 8: Apply Controller, Function, Table ACLs, Entity Realm + Hierarchy and Delegations
#
settings.security.policy = 7 # Organisation-ACLs

# RSS feeds
#settings.frontpage.rss = [
#    {"title": "Eden",
#     # Trac timeline
#     "url": "http://eden.sahanafoundation.org/timeline?ticket=on&changeset=on&milestone=on&wiki=on&max=50&daysback=90&format=rss"
#    },
#    {"title": "Twitter",
#     # @SahanaFOSS
#     #"url": "https://search.twitter.com/search.rss?q=from%3ASahanaFOSS" # API v1 deprecated, so doesn't work, need to use 3rd-party service, like:
#     "url": "http://www.rssitfor.me/getrss?name=@SahanaFOSS"
#     # Hashtag
#     #url: "http://search.twitter.com/search.atom?q=%23eqnz" # API v1 deprecated, so doesn't work, need to use 3rd-party service, like:
#     #url: "http://api2.socialmention.com/search?q=%23eqnz&t=all&f=rss"
#    }
#]

# -----------------------------------------------------------------------------
# Summary Pages
settings.ui.summary = [#{"common": True,
                       # "name": "cms",
                       # "widgets": [{"method": "cms"}]
                       # },
                      {"common": True,
                        "name": "add",
                        "widgets": [{"method": "create"}],
                        },
                       {"name": "table",
                        "label": "Table",
                        "widgets": [{"method": "datatable"}]
                        },
                       {"name": "map",
                        "label": "Map",
                        "widgets": [{"method": "map", "ajax_init": True}],
                        },
                       {"name": "charts",
                        "label": "Reports",
                        "widgets": [{"method": "report", "ajax_init": True}]
                        },
                       ]

settings.search.filter_manager = False

# -----------------------------------------------------------------------------
# Template config
settings.inv.direct_stock_edits = True
#settings.req_type = ["Stock"]

# -----------------------------------------------------------------------------
def customise_req_req_resource(r, tablename):
    s3 = current.response.s3
    s3db = current.s3db
    table = s3db[tablename]
    table.site_id.label = "Location Needed"
    s3.crud_strings[tablename] = Storage(
        label_create = T("Post a Need"),
        title_display = T("Posted Need Details"),
        title_list = T("Posted Needs"),
        title_map=T("Map of Posted Needs"),
        title_report = T("Posted Need Report"),
        title_update = T("Edit Need"),
        label_list_button = T("List Need"),
        label_delete_button = T("Delete Need"),
        msg_record_created = T("Need Posted"),
        msg_record_modified = T("Need Updated"),
        msg_record_deleted = T("Need Canceled"),
        msg_list_empty = T("No Needs Posted"))

    s3db.configure(tablename,
                   listadd = True,
                   )

settings.customise_req_req_resource = customise_req_req_resource
# -----------------------------------------------------------------------------
def customise_req_req_item_resource(r, tablename):
    s3 = current.response.s3
    s3db = current.s3db
    table = s3db[tablename]
    s3.crud_strings[tablename] = Storage(
        label_create = T("Post a Need"),
        title_display = T("Posted Need Details"),
        title_list = T("Posted Needs"),
        title_map=T("Map of Posted Needs"),
        title_report = T("Posted Need Report"),
        title_update = T("Edit Need"),
        label_list_button = T("List Need"),
        label_delete_button = T("Delete Need"),
        msg_record_created = T("Need Posted"),
        msg_record_modified = T("Need Updated"),
        msg_record_deleted = T("Need Canceled"),
        msg_list_empty = T("No Needs Posted"))

settings.customise_req_req_item_resource = customise_req_req_item_resource

# -----------------------------------------------------------------------------
def customise_inv_inv_item_controller(**attr):
    s3 = current.response.s3
    s3db = current.s3db
    tablename = "inv_inv_item"
    table = s3db[tablename]

    s3.crud_strings[tablename] = Storage(
        label_create = T("Make a General Offer"),
        title_display = T("General Offer"),
        title_list = T("General Offers"),
        title_update = T("Edit General Offer"),
        label_list_button = T("List General Offer"),
        label_delete_button = T("Remove General Offer"),
        msg_record_created = T("General Offer added"),
        msg_record_modified = T("General Offer updated"),
        msg_record_deleted = T("General Offer removed"),
        msg_list_empty = T("No General Offers currently recorded"))

    list_fields = ["person_id",
                   "site_id",
                   "item_id",
                   "item_pack_id",
                   "quantity",
                   "expiry_date",
                   "pack_value",
                   #"owner_org_id",
                   "comments",
                   ]

    crud_form = S3SQLCustomForm(*list_fields)

    s3db.configure(tablename,
                   addbtn = True,
                   listadd = True,
                   list_fields = list_fields,
                   crud_form = crud_form,
                   )
    return attr

settings.customise_inv_inv_item_controller = customise_inv_inv_item_controller
# -----------------------------------------------------------------------------
def customise_org_facility_resource(r, tablename):
    # CRUD strings
    current.response.s3.crud_strings[tablename] = Storage(
        label_create = T("Create Warehouse"),
        title_display = T("Warehouse Details"),
        title_list = T("Warehouses"),
        title_update = T("Edit Warehouse"),
        title_upload = T("Import Warehouses"),
        title_map = T("Map of Warehouses"),
        label_list_button = T("List Warehouses"),
        label_delete_button = T("Delete Warehouse"),
        msg_record_created = T("Warehouse added"),
        msg_record_modified = T("Warehouse updated"),
        msg_record_deleted = T("Warehouse deleted"),
        msg_list_empty = T("No Warehouses currently registered"))

    current.s3db.configure("inv_inv_item",
                   addbtn = True,
                   listadd = True,
                   )
settings.customise_org_facility_resource = customise_org_facility_resource
# -----------------------------------------------------------------------------
# Comment/uncomment modules here to disable/enable them
# Modules menu is defined in modules/eden/menu.py
settings.modules = OrderedDict([
    # Core modules which shouldn't be disabled
    ("default", Storage(
        name_nice = T("Home"),
        restricted = False, # Use ACLs to control access to this module
        access = None,      # All Users (inc Anonymous) can see this module in the default menu & access the controller
        module_type = None  # This item is not shown in the menu
    )),
    ("admin", Storage(
        name_nice = T("Administration"),
        #description = "Site Administration",
        restricted = True,
        access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
        module_type = None  # This item is handled separately for the menu
    )),
    ("appadmin", Storage(
        name_nice = T("Administration"),
        #description = "Site Administration",
        restricted = True,
        module_type = None  # No Menu
    )),
    ("errors", Storage(
        name_nice = T("Ticket Viewer"),
        #description = "Needed for Breadcrumbs",
        restricted = False,
        module_type = None  # No Menu
    )),
    #("sync", Storage(
    #    name_nice = T("Synchronization"),
    #    #description = "Synchronization",
    #    restricted = True,
    #    access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
    #    module_type = None  # This item is handled separately for the menu
    #)),
    #("tour", Storage(
    #    name_nice = T("Guided Tour Functionality"),
    #    module_type = None,
    #)),
    #("translate", Storage(
    #    name_nice = T("Translation Functionality"),
    #    #description = "Selective translation of strings based on module.",
    #    module_type = None,
    #)),
    ("gis", Storage(
        name_nice = T("Map"),
        #description = "Situation Awareness & Geospatial Analysis",
        restricted = True,
        module_type = 6,     # 6th item in the menu
    )),
    ("pr", Storage(
        name_nice = T("Person Registry"),
        #description = "Central point to record details on People",
        restricted = True,
        access = "|1|",     # Only Administrators can see this module in the default menu (access to controller is possible to all still)
        module_type = 10
    )),
    ("org", Storage(
        name_nice = T("Organizations"),
        #description = 'Lists "who is doing what & where". Allows relief agencies to coordinate their activities',
        restricted = True,
        module_type = 1
    )),
    ("hrm", Storage(
        name_nice = T("Staff"),
        #description = "Human Resources Management",
        restricted = True,
        module_type = 2,
    )),
    ("vol", Storage(
        name_nice = T("Volunteers"),
        #description = "Human Resources Management",
        restricted = True,
        module_type = 2,
    )),
    #("cms", Storage(
    #  name_nice = T("Content Management"),
    #  #description = "Content Management System",
    #  restricted = True,
    #  module_type = 10,
    #)),
    #("doc", Storage(
    #    name_nice = T("Documents"),
    #    #description = "A library of digital resources, such as photos, documents and reports",
    #    restricted = True,
    #    module_type = 10,
    #)),
    #("msg", Storage(
    #    name_nice = T("Messaging"),
    #    #description = "Sends & Receives Alerts via Email & SMS",
    #    restricted = True,
    #    # The user-visible functionality of this module isn't normally required. Rather it's main purpose is to be accessed from other modules.
    #    module_type = None,
    #)),
    ("supply", Storage(
        name_nice = T("Supply Chain Management"),
        #description = "Used within Inventory Management, Request Management and Asset Management",
        restricted = True,
        module_type = None, # Not displayed
    )),
    ("inv", Storage(
        name_nice = T("Warehouses"),
        #description = "Receiving and Sending Items",
        restricted = True,
        module_type = 4
    )),
    #("asset", Storage(
    #    name_nice = T("Assets"),
    #    #description = "Recording and Assigning Assets",
    #    restricted = True,
    #    module_type = 5,
    #)),
    # Vehicle depends on Assets
    #("vehicle", Storage(
    #    name_nice = T("Vehicles"),
    #    #description = "Manage Vehicles",
    #    restricted = True,
    #    module_type = 10,
    #)),
    ("req", Storage(
        name_nice = T("Requests"),
        #description = "Manage requests for supplies, assets, staff or other resources. Matches against Inventories where supplies are requested.",
        restricted = True,
        module_type = 10,
    )),
    #("project", Storage(
    #    name_nice = T("Projects"),
    #    #description = "Tracking of Projects, Activities and Tasks",
    #    restricted = True,
    #    module_type = 2
    #)),
    #("cr", Storage(
    #    name_nice = T("Shelters"),
    #    #description = "Tracks the location, capacity and breakdown of victims in Shelters",
    #    restricted = True,
    #    module_type = 10
    #)),
    #("hms", Storage(
    #    name_nice = T("Hospitals"),
    #    #description = "Helps to monitor status of hospitals",
    #    restricted = True,
    #    module_type = 10
    #)),
    #("dvr", Storage(
    #   name_nice = T("Disaster Victim Registry"),
    #   #description = "Allow affected individuals & households to register to receive compensation and distributions",
    #   restricted = True,
    #   module_type = 10,
    #)),
    #("event", Storage(
    #    name_nice = T("Events"),
    #    #description = "Activate Events (e.g. from Scenario templates) for allocation of appropriate Resources (Human, Assets & Facilities).",
    #    restricted = True,
    #    module_type = 10,
    #)),
    #("transport", Storage(
    #   name_nice = T("Transport"),
    #   restricted = True,
    #   module_type = 10,
    #)),
    #("stats", Storage(
    #    name_nice = T("Statistics"),
    #    #description = "Manages statistics",
    #    restricted = True,
    #    module_type = None,
    #)),
])
