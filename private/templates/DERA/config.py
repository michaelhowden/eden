# -*- coding: utf-8 -*-

try:
    # Python 2.7
    from collections import OrderedDict
except:
    # Python 2.6
    from gluon.contrib.simplejson.ordered_dict import OrderedDict

from gluon import current
from gluon.html import *
from gluon.storage import Storage
from gluon.validators import IS_NOT_EMPTY

from s3.s3fields import S3Represent
from s3.s3query import FS
from s3.s3utils import S3DateTime, s3_auth_user_represent_name, s3_avatar_represent
from s3.s3validators import IS_LOCATION_SELECTOR2, IS_ONE_OF
from s3.s3widgets import S3LocationSelectorWidget2
from s3.s3forms import S3SQLCustomForm, S3SQLInlineComponent, S3SQLInlineComponentMultiSelectWidget

T = current.T
s3 = current.response.s3
settings = current.deployment_settings

datetime_represent = lambda dt: S3DateTime.datetime_represent(dt, utc=True)

"""
    Template settings for Requests Management
    - for Philippines
"""

# -----------------------------------------------------------------------------
# Pre-Populate
settings.base.prepopulate = ("DERA", "default/users")

settings.base.system_name = T("Sahana")
settings.base.system_name_short = T("Sahana")

# =============================================================================
# System Settings
# -----------------------------------------------------------------------------
# Authorization Settings
# Users can self-register
#settings.security.self_registration = False
# Users need to verify their email
settings.auth.registration_requires_verification = True
# Users don't need to be approved
#settings.auth.registration_requires_approval = True
# Organisation links are either done automatically
# - by registering with official domain of Org
# or Manually by Call Center staff
#settings.auth.registration_requests_organisation = True
#settings.auth.registration_organisation_required = True
settings.auth.registration_requests_site = False
# Uncomment this to allow Admin to see Organisations in user Admin even if the Registration doesn't request this
settings.auth.admin_sees_organisation = True

# Approval emails get sent to all admins
settings.mail.approver = "ADMIN"

settings.auth.registration_link_user_to = {"staff": T("Staff")}
settings.auth.registration_link_user_to_default = ["staff"]
settings.auth.registration_roles = {"organisation_id": ["USER"],
                                    }

# Terms of Service to be able to Register on the system
# uses <template>/views/tos.html
settings.auth.terms_of_service = True

settings.auth.show_utc_offset = False

settings.auth.show_link = False

# -----------------------------------------------------------------------------
# Security Policy
settings.security.policy = 5 # Apply Controller, Function and Table ACLs
settings.security.map = True

# Owner Entity
settings.auth.person_realm_human_resource_site_then_org = False

# -----------------------------------------------------------------------------
# Theme (folder to use for views/layout.html)
settings.base.theme = "DERA"
settings.ui.formstyle_row = "bootstrap"
settings.ui.formstyle = "bootstrap"
settings.ui.filter_formstyle = "bootstrap"
#settings.gis.map_height = 600
#settings.gis.map_width = 854

# -----------------------------------------------------------------------------
# L10n (Localization) settings
settings.L10n.languages = OrderedDict([
    ("en", "English"),
#    ("tl", "Tagalog"),
])
# Default Language
settings.L10n.default_language = "en"
# Default timezone for users
settings.L10n.utc_offset = "UTC +0800"
# Unsortable 'pretty' date format
settings.L10n.date_format = "%d %b %Y"
# Number formats (defaults to ISO 31-0)
# Decimal separator for numbers (defaults to ,)
settings.L10n.decimal_separator = "."
# Thousands separator for numbers (defaults to space)
settings.L10n.thousands_separator = ","

# Uncomment this to Translate CMS Series Names
# - we want this on when running s3translate but off in normal usage as we use the English names to lookup icons in render_posts
#settings.L10n.translate_cms_series = True
# Uncomment this to Translate Location Names
#settings.L10n.translate_gis_location = True

# Restrict the Location Selector to just certain countries
settings.gis.countries = ["PH"]

# Until we add support to LocationSelector2 to set dropdowns from LatLons
#settings.gis.check_within_parent_boundaries = False
# Uncomment to hide Layer Properties tool
#settings.gis.layer_properties = False
# Uncomment to display the Map Legend as a floating DIV
settings.gis.legend = "float"

# -----------------------------------------------------------------------------
# Finance settings
settings.fin.currencies = {
    #"EUR" : T("Euros"),
    #"GBP" : T("Great British Pounds"),
    #"CHF" : T("Swiss Francs"),
    "USD" : T("United States Dollars"),
}
settings.fin.currency_default = "PHP"

# -----------------------------------------------------------------------------
# Enable this for a UN-style deployment
#settings.ui.cluster = True
# Enable this to use the label 'Camp' instead of 'Shelter'
#settings.ui.camp = True

# -----------------------------------------------------------------------------
# Uncomment to restrict the export formats available
#settings.ui.export_formats = ["xls"]

settings.ui.update_label = "Edit"

# -----------------------------------------------------------------------------
# Summary Pages
settings.ui.summary = [#{"common": True,
                       # "name": "cms",
                       # "widgets": [{"method": "cms"}]
                       # },
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

# Filter forms - style for Summary pages
#def filter_formstyle(row_id, label, widget, comment, hidden=False):
#    return DIV(label, widget, comment, 
#               _id=row_id,
#               _class="horiz_filter_form")

# =============================================================================
# Module Settings

# -----------------------------------------------------------------------------
# Human Resource Management
settings.hrm.staff_label = "Personnel"
# Uncomment to allow Staff & Volunteers to be registered without an organisation
settings.hrm.org_required = False
# Uncomment to allow Staff & Volunteers to be registered without an email address
settings.hrm.email_required = False
# Uncomment to show the Organisation name in HR represents
settings.hrm.show_organisation = True
# Uncomment to disable Staff experience
settings.hrm.staff_experience = False
# Uncomment to disable the use of HR Credentials
settings.hrm.use_credentials = False
# Uncomment to disable the use of HR Skills
settings.hrm.use_skills = False
# Uncomment to disable the use of HR Teams
settings.hrm.teams = False

# Uncomment to hide fields in S3AddPersonWidget[2]
settings.pr.request_dob = False
settings.pr.request_gender = False

# -----------------------------------------------------------------------------
# Org
#settings.org.site_label = "Office/Shelter/Hospital"
settings.org.site_label = "Site"
settings.org.site_autocomplete = True
# Extra fields to show in Autocomplete Representations
settings.org.site_autocomplete_fields = ["location_id$L1",
                                         "location_id$L2",
                                         "location_id$L3",
                                         "location_id$L4",
                                         ]

# -----------------------------------------------------------------------------
# Project
# Uncomment this to use multiple Organisations per project
settings.project.multiple_organisations = True

# Links to Filtered Components for Donors & Partners
#settings.project.organisation_roles = {
#    1: T("Host National Society"),
#    2: T("Partner"),
#    3: T("Donor"),
#    #4: T("Customer"), # T("Beneficiary")?
#    #5: T("Supplier"),
#    9: T("Partner National Society"),
#}

# -----------------------------------------------------------------------------
# Notifications
# Template for the subject line in update notifications
#settings.msg.notify_subject = "$S %s" % T("Notification")
settings.msg.notify_subject = "$S Notification"

# -----------------------------------------------------------------------------
# CMS
settings.cms.show_series = False
settings.cms.show_locations = False
settings.cms.show_eventss = True

# -----------------------------------------------------------------------------
def currency_represent(v):
    """
        Custom Representation of Currencies
    """

    if v == "USD":
        return "$"
    elif v == "EUR":
        return "€"
    elif v == "GBP":
        return "£"
    else:
        # e.g. CHF
        return v

# -----------------------------------------------------------------------------
def render_contacts(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Contacts on the Profile pages

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["hrm_human_resource.id"]
    item_class = "thumbnail"

    raw = record._row
    #author = record["hrm_human_resource.modified_by"]
    date = record["hrm_human_resource.modified_on"]
    fullname = record["hrm_human_resource.person_id"]
    job_title = raw["hrm_human_resource.job_title_id"] or ""
    if job_title:
        job_title = "- %s" % record["hrm_human_resource.job_title_id"]
    #organisation = record["hrm_human_resource.organisation_id"]
    organisation_id = raw["hrm_human_resource.organisation_id"]
    #org_url = URL(c="org", f="organisation", args=[organisation_id, "profile"])
    pe_id = raw["pr_person.pe_id"]
    person_id = raw["hrm_human_resource.person_id"]
    location = record["org_site.location_id"]
    location_id = raw["org_site.location_id"]
    location_url = URL(c="gis", f="location",
                       args=[location_id, "profile"])
    address = raw["gis_location.addr_street"] or T("no office assigned")
    email = raw["pr_email_contact.value"] or T("no email address")
    if isinstance(email, list):
        email = email[0]
    phone = raw["pr_phone_contact.value"] or T("no phone number")
    if isinstance(phone, list):
        phone = phone[0]

    db = current.db
    s3db = current.s3db
    ltable = s3db.pr_person_user
    query = (ltable.pe_id == pe_id)
    row = db(query).select(ltable.user_id,
                           limitby=(0, 1)
                           ).first()
    if row:
        # Use Personal Avatar
        # @ToDo: Optimise by not doing DB lookups (especially duplicate) within render, but doing these in the bulk query
        avatar = s3_avatar_represent(row.user_id,
                                     _class="media-object")
    else:
        avatar = IMG(_src=URL(c="static", f="img", args="blank-user.gif"),
                     _class="media-object")

    # Edit Bar
    permit = current.auth.s3_has_permission
    table = db.pr_person
    if permit("update", table, record_id=person_id):
        vars = {"refresh": list_id,
                "record": record_id,
                }
        f = current.request.function
        if f == "organisation" and organisation_id:
            vars["(organisation)"] = organisation_id
        edit_url = URL(c="hrm", f="person",
                       args=[person_id, "update.popup"],
                       vars=vars)
        title_update = current.response.s3.crud_strings.hrm_human_resource.title_update
        edit_btn = A(I(" ", _class="icon icon-edit"),
                     _href=edit_url,
                     _class="s3_modal",
                     _title=title_update,
                     )
    else:
        edit_btn = ""
        edit_url = "#"
        title_update = ""
    # Deletions failing due to Integrity Errors
    #if permit("delete", table, record_id=person_id):
    #    delete_btn = A(I(" ", _class="icon icon-trash"),
    #                   _class="dl-item-delete",
    #                   )
    #else:
    delete_btn = ""
    edit_bar = DIV(edit_btn,
                   delete_btn,
                   _class="edit-bar fright",
                   )

    avatar = A(avatar,
               _href=edit_url,
               _class="pull-left s3_modal",
               _title=title_update,
               )

    # Render the item
    body = TAG[""](P(fullname,
                     " ",
                     SPAN(job_title),
                     _class="person_pos",
                     ),
                   P(I(_class="icon-phone"),
                     " ",
                     SPAN(phone),
                     " ",
                     I(_class="icon-envelope-alt"),
                     " ",
                     SPAN(email),
                     _class="card_1_line",
                     ),
                   P(I(_class="icon-home"),
                     " ",
                     address,
                     _class="card_manylines",
                     ))

    item = DIV(DIV(SPAN(" ", _class="card-title"),
                   SPAN(A(location,
                          _href=location_url,
                          ),
                        _class="location-title",
                        ),
                   SPAN(date,
                        _class="date-title",
                        ),
                   edit_bar,
                   _class="card-header",
                   ),
               DIV(avatar,
                   DIV(DIV(body,
                           # Organisation only needed if displaying elsewhere than org profile
                           # Author confusing with main contact record
                           #DIV(#author,
                           #    #" - ",
                           #    A(organisation,
                           #      _href=org_url,
                           #      _class="card-organisation",
                           #      ),
                           #    _class="card-person",
                           #    ),
                           _class="media",
                           ),
                       _class="media-body",
                       ),
                   _class="media",
                   ),
               #docs,
               _class=item_class,
               _id=item_id,
               )

    return item

# -----------------------------------------------------------------------------
def quote_unicode(s):
    """
        Quote unicode strings for URLs for Rocket
    """

    chars = []
    for char in s:
        o = ord(char)
        if o < 128:
            chars.append(char)
        else:
            chars.append(hex(o).replace("0x", "%").upper())
    return "".join(chars)

# -----------------------------------------------------------------------------
def render_locations(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Locations on the Selection Page

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """
    
    record_id = record["gis_location.id"]
    item_class = "thumbnail"

    raw = record._row
    name = raw["gis_location.name"]
    level = raw["gis_location.level"]
    L1 = raw["gis_location.L1"]
    L2 = raw["gis_location.L2"]
    L3 = raw["gis_location.L3"]
    L4 = raw["gis_location.L4"]
    location_url = URL(c="gis", f="location",
                       args=[record_id, "profile"])

    if level == "L1":
        represent = name
    if level == "L2":
        represent = "%s (%s)" % (name, L1)
    elif level == "L3":
        represent = "%s (%s, %s)" % (name, L2, L1)
    elif level == "L4":
        represent = "%s (%s, %s, %s)" % (name, L3, L2, L1)
    else:
        # L0 or specific
        represent = name

    # Users don't edit locations
    # permit = current.auth.s3_has_permission
    # table = current.db.gis_location
    # if permit("update", table, record_id=record_id):
        # edit_btn = A(I(" ", _class="icon icon-edit"),
                     # _href=URL(c="gis", f="location",
                               # args=[record_id, "update.popup"],
                               # vars={"refresh": list_id,
                                     # "record": record_id}),
                     # _class="s3_modal",
                     # _title=current.response.s3.crud_strings.gis_location.title_update,
                     # )
    # else:
        # edit_btn = ""
    # if permit("delete", table, record_id=record_id):
        # delete_btn = A(I(" ", _class="icon icon-trash"),
                       # _class="dl-item-delete",
                      # )
    # else:
        # delete_btn = ""
    # edit_bar = DIV(edit_btn,
                   # delete_btn,
                   # _class="edit-bar fright",
                   # )

    # Tallies
    # NB We assume that all records are readable here
    # Search all sub-locations
    locations = current.gis.get_children(record_id)
    locations = [l.id for l in locations]
    locations.append(record_id)
    db = current.db
    s3db = current.s3db
    stable = s3db.org_site
    query = (stable.deleted == False) & \
            (stable.location_id.belongs(locations))
    count = stable.id.count()
    row = db(query).select(count).first()
    if row:
        tally_sites = row[count]
    else:
        tally_sites = 0

    table = s3db.req_req
    query = (table.deleted == False) & \
            (stable.site_id == table.site_id) & \
            (stable.location_id.belongs(locations))
    count = table.id.count()
    row = db(query).select(count).first()
    if row:
        tally_reqs = row[count]
    else:
        tally_reqs = 0

    table = s3db.req_commit
    query = (table.deleted == False) & \
            (table.location_id.belongs(locations))
    count = table.id.count()
    row = db(query).select(count).first()
    if row:
        tally_commits = row[count]
    else:
        tally_commits = 0

    if level == "L4":
        next_Lx = ""
        next_Lx_label = ""
    else:
        if level == "L0":
            next_Lx = "L1"
            next_Lx_label = "Regions"
        if level == "L1":
            next_Lx = "L2"
            next_Lx_label = "Provinces"
        elif level == "L2":
            next_Lx = "L3"
            next_Lx_label = "Municipalities / Cities"
        elif level == "L3":
            next_Lx = "L4"
            next_Lx_label = "Barangays"
        table = db.gis_location
        query = (table.deleted == False) & \
                (table.level == next_Lx) & \
                (table.parent == record_id)
        count = table.id.count()
        row = db(query).select(count).first()
        if row:
            tally_Lx = row[count]
        else:
            tally_Lx = 0
        next_url = URL(c="gis", f="location",
                       args=["datalist"],
                       vars={"~.level": next_Lx,
                             "~.parent": record_id,
                             })
        next_Lx_label = A(next_Lx_label,
                          _href=next_url,
                          )
        next_Lx = SPAN(tally_Lx,
                       _class="badge",
                       )

    # Build the icon, if it doesn't already exist
    filename = "%s.svg" % record_id
    import os
    filepath = os.path.join(current.request.folder, "static", "cache", "svg", filename)
    if not os.path.exists(filepath):
        gtable = db.gis_location
        loc = db(gtable.id == record_id).select(gtable.wkt,
                                                limitby=(0, 1)
                                                ).first()
        if loc:
            from s3.s3codecs.svg import S3SVG
            S3SVG.write_file(filename, loc.wkt)

    # Render the item
    item = DIV(DIV(A(IMG(_class="media-object",
                         _src=URL(c="static",
                                  f="cache",
                                  args=["svg", filename],
                                  )
                         ),
                     _class="pull-left",
                     _href=location_url,
                     ),
                   DIV(SPAN(A(represent,
                              _href=location_url,
                              _class="media-heading"
                              ),
                            ),
                       #edit_bar,
                       _class="card-header-select",
                       ),
                   DIV(P(next_Lx_label,
                         next_Lx,
                         T("Sites"),
                         SPAN(tally_sites,
                              _class="badge",
                              ),
                         T("Requests"),
                         SPAN(tally_reqs,
                              _class="badge",
                              ),
                         T("Donations"),
                         SPAN(tally_commits,
                              _class="badge",
                              ),
                         _class="tally",
                         ),
                       _class="media-body",
                       ),
                   _class="media",
                   ),
               _class=item_class,
               _id=item_id,
               )

    return item

# -----------------------------------------------------------------------------
def render_locations_profile(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Locations on the Profile Page
        - UNUSED

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["gis_location.id"]
    item_class = "thumbnail"

    raw = record._row
    name = record["gis_location.name"]
    location_url = URL(c="gis", f="location",
                       args=[record_id, "profile"])

    # Placeholder to maintain style
    #logo = DIV(IMG(_class="media-object"),
    #               _class="pull-left")

    # We don't Edit Locations
    # Edit Bar
    # permit = current.auth.s3_has_permission
    # table = current.db.gis_location
    # if permit("update", table, record_id=record_id):
        # vars = {"refresh": list_id,
                # "record": record_id,
                # }
        # f = current.request.function
        # if f == "organisation" and organisation_id:
            # vars["(organisation)"] = organisation_id
        # edit_btn = A(I(" ", _class="icon icon-edit"),
                     # _href=URL(c="gis", f="location",
                               # args=[record_id, "update.popup"],
                               # vars=vars),
                     # _class="s3_modal",
                     # _title=current.response.s3.crud_strings.gis_location.title_update,
                     # )
    # else:
        # edit_btn = ""
    # if permit("delete", table, record_id=record_id):
        # delete_btn = A(I(" ", _class="icon icon-trash"),
                       # _class="dl-item-delete",
                       # )
    # else:
        # delete_btn = ""
    # edit_bar = DIV(edit_btn,
                   # delete_btn,
                   # _class="edit-bar fright",
                   # )

    # Render the item
    item = DIV(DIV(DIV(#SPAN(A(name,
                       #       _href=location_url,
                       #       ),
                       #     _class="location-title"),
                       #" ",
                       #edit_bar,
                       P(A(name,
                           _href=location_url,
                           ),
                         _class="card_comments"),
                       _class="span5"), # card-details
                   _class="row",
                   ),
               )

    return item

# -----------------------------------------------------------------------------
def render_sites(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Facilities on the Profile pages

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["org_facility.id"]
    item_class = "thumbnail"

    raw = record._row
    name = record["org_facility.name"]
    site_id = raw["org_facility.id"]
    opening_times = raw["org_facility.opening_times"] or ""
    author = record["org_facility.modified_by"]
    date = record["org_facility.modified_on"]
    organisation = record["org_facility.organisation_id"]
    organisation_id = raw["org_facility.organisation_id"]
    location = record["org_facility.location_id"]
    level = raw["gis_location.level"]
    if level:
        location_id = raw["org_facility.location_id"]
    else:
        location_id = raw["gis_location.parent"]
    location_url = URL(c="gis", f="location",
                       args=[location_id, "profile"])
    address = raw["gis_location.addr_street"] or ""
    phone = raw["org_facility.phone1"] or ""
    facility_type = record["org_site_facility_type.facility_type_id"]
    comments = record["org_facility.comments"] or ""
    logo = raw["org_organisation.logo"]

    site_url = URL(c="org", f="facility", args=[site_id, "profile"])
    org_url = URL(c="org", f="organisation", args=[organisation_id, "profile"])
    if logo:
        logo = A(IMG(_src=URL(c="default", f="download", args=[logo]),
                     _class="media-object",
                     ),
                 _href=org_url,
                 _class="pull-left",
                 )
    else:
        logo = DIV(IMG(_class="media-object"),
                   _class="pull-left")

    facility_status = raw["org_site_status.facility_status"] or ""
    if facility_status:
        if facility_status == 1:
            icon = "thumbs-up-alt"
            colour = "green"
        elif facility_status == 2:
            icon = "thumbs-down-alt"
            colour = "amber"
        elif facility_status == 3:
            icon = "reply-all"
            colour = "red"
        elif facility_status == 4:
            icon = "remove"
            colour = "red"
        elif facility_status == 99:
            icon = "question"
            colour = ""
        facility_status = P(#I(_class="icon-%s" % icon),
                            #" ",
                            SPAN("%s: %s" % (T("Status"), record["org_site_status.facility_status"])),
                            " ",
                            _class="card_1_line %s" % colour,
                            )
    power_supply_type = raw["org_site_status.power_supply_type"] or ""
    if power_supply_type:
        if power_supply_type == 1:
            icon = "thumbs-up-alt"
            colour = "green"
        elif power_supply_type == 2:
            icon = "cogs"
            colour = "amber"
        elif power_supply_type == 98:
            icon = "question"
            colour = "amber"
        elif power_supply_type == 99:
            icon = "remove"
            colour = "red"
        power_supply_type = P(#I(_class="icon-%s" % icon),
                              #" ",
                              SPAN("%s: %s" % (T("Power"), record["org_site_status.power_supply_type"])),
                              " ",
                              _class="card_1_line %s" % colour,
                              )

    # Edit Bar
    permit = current.auth.s3_has_permission
    table = current.db.org_facility
    if permit("update", table, record_id=record_id):
        vars = {"refresh": list_id,
                "record": record_id,
                }
        f = current.request.function
        if f == "organisation" and organisation_id:
            vars["(organisation)"] = organisation_id
        edit_btn = A(I(" ", _class="icon icon-edit"),
                     _href=URL(c="org", f="facility",
                               args=[record_id, "update.popup"],
                               vars=vars),
                     _class="s3_modal",
                     _title=current.response.s3.crud_strings.org_facility.title_update,
                     )
    else:
        edit_btn = ""
    if permit("delete", table, record_id=record_id):
        delete_btn = A(I(" ", _class="icon icon-trash"),
                       _class="dl-item-delete",
                       )
    else:
        delete_btn = ""
    edit_bar = DIV(edit_btn,
                   delete_btn,
                   _class="edit-bar fright",
                   )

    # Render the item
    body = TAG[""](P(I(_class="icon-flag"),
                     " ",
                     SPAN(facility_type),
                     " ",
                     _class="card_1_line",
                     ),
                   P(I(_class="icon-home"),
                     " ",
                     address,
                     _class="card_manylines",
                     ),
                   P(I(_class="icon-time"),
                     " ",
                     SPAN(opening_times),
                     " ",
                     _class="card_1_line",
                     ),
                   P(I(_class="icon-phone"),
                     " ",
                     SPAN(phone),
                     " ",
                     _class="card_1_line",
                     ),
                   facility_status,
                   power_supply_type,
                   P(comments,
                     _class="card_manylines s3-truncate",
                     ),
                   )

    item = DIV(DIV(SPAN(A(name,
                          _href=site_url,
                          ),
                        _class="card-title",
                        ),
                   SPAN(A(location,
                          _href=location_url,
                          ),
                        _class="location-title",
                        ),
                   SPAN(date,
                        _class="date-title",
                        ),
                   edit_bar,
                   _class="card-header",
                   ),
               DIV(logo,
                   DIV(DIV(body,
                           DIV(author,
                               " - ",
                               A(organisation,
                                 _href=org_url,
                                 _class="card-organisation",
                                 ),
                               _class="card-person",
                               ),
                           _class="media",
                           ),
                       _class="media-body",
                       ),
                   _class="media",
                   ),
               #docs,
               _class=item_class,
               _id=item_id,
               )

    return item

# -----------------------------------------------------------------------------
def render_organisations(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Organisations on the Stakeholder Selection Page

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["org_organisation.id"]
    item_class = "thumbnail span6" # span6 for 2 cols

    raw = record._row
    name = record["org_organisation.name"]
    logo = raw["org_organisation.logo"]
    phone = raw["org_organisation.phone"] or ""
    website = raw["org_organisation.website"] or ""
    if website:
        website = A(website, _href=website)
    money = raw["req_organisation_needs.money"]
    if money:
        money_details = record["req_organisation_needs.money_details"]
        money_details = SPAN(XML(money_details),
                             _class="s3-truncate")
        money_details = P(I(_class="icon icon-dollar"),
                          " ",
                          money_details,
                          _class="card_manylines",
                          )
    else:
        # Include anyway to make cards align
        money_details = P(I(_class="icon icon-dollar"),
                          " ",
                          _class="card_1_line",
                          )
    #time = raw["req_organisation_needs.vol"]
    #if time:
    #    time_details = record["req_organisation_needs.vol_details"]
    #    time_details = P(I(_class="icon icon-time"),
    #                     " ",
    #                    XML(time_details),
    #                     _class="card_1_line",
    #                     )
    #else:
    #    time_details = ""

    org_url = URL(c="org", f="organisation", args=[record_id, "profile"])
    if logo:
        logo = A(IMG(_src=URL(c="default", f="download", args=[logo]),
                     _class="media-object",
                     ),
                 _href=org_url,
                 _class="pull-left",
                 )
    else:
        logo = DIV(IMG(_class="media-object"),
                   _class="pull-left")

    db = current.db
    permit = current.auth.s3_has_permission
    table = db.org_organisation
    if permit("update", table, record_id=record_id):
        edit_btn = A(I(" ", _class="icon icon-edit"),
                     _href=URL(c="org", f="organisation",
                               args=[record_id, "update.popup"],
                               vars={"refresh": list_id,
                                     "record": record_id}),
                     _class="s3_modal",
                     _title=current.response.s3.crud_strings.org_organisation.title_update,
                     )
    else:
        edit_btn = ""
    if permit("delete", table, record_id=record_id):
        delete_btn = A(I(" ", _class="icon icon-trash"),
                       _class="dl-item-delete",
                      )
    else:
        delete_btn = ""
    edit_bar = DIV(edit_btn,
                   delete_btn,
                   _class="edit-bar fright",
                   )

    # Tallies
    # NB We assume that all records are readable here
    s3db = current.s3db
    stable = s3db.org_site
    query = (stable.deleted == False) & \
            (stable.obsolete == False) & \
            (stable.organisation_id == record_id)
    tally_sites = db(query).count()

    table = s3db.req_req
    query = (table.deleted == False) & \
            (stable.site_id == table.site_id) & \
            (stable.organisation_id == record_id)
    tally_reqs = db(query).count()

    table = s3db.req_commit
    query = (table.deleted == False) & \
            (table.organisation_id == record_id)
    tally_commits = db(query).count()

    # Render the item
    item = DIV(DIV(logo,
                   DIV(SPAN(A(name,
                              _href=org_url,
                              _class="media-heading"
                              ),
                            ),
                       edit_bar,
                       _class="card-header-select",
                       ),
                   DIV(P(I(_class="icon icon-phone"),
                         " ",
                         phone,
                         _class="card_1_line",
                         ),
                       P(I(_class="icon icon-map"),
                         " ",
                         website,
                         _class="card_1_line",
                         ),
                       money_details,
                       #time_details,
                       P(T("Sites"),
                         SPAN(tally_sites,
                              _class="badge",
                              ),
                         T("Requests"),
                         SPAN(tally_reqs,
                              _class="badge",
                              ),
                         T("Donations"),
                         SPAN(tally_commits,
                              _class="badge",
                              ),
                         _class="tally",
                         ),
                       _class="media-body",
                       ),
                   _class="media",
                   ),
               _class=item_class,
               _id=item_id,
               )

    return item

# -----------------------------------------------------------------------------
def render_org_needs(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Needs
        - UNUSED

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["req_organisation_needs.id"]
    item_class = "thumbnail"

    raw = record._row
    logo = raw["org_organisation.logo"]
    phone = raw["org_organisation.phone"] or ""
    website = raw["org_organisation.website"] or ""
    if website:
        website = A(website, _href=website)
    author = record["req_organisation_needs.modified_by"]
    date = record["req_organisation_needs.modified_on"]
    money = raw["req_organisation_needs.money"]
    if money:
        money_details = record["req_organisation_needs.money_details"]
        money_details = P(I(_class="icon icon-dollar"),
                          " ",
                          XML(money_details),
                          _class="card_manylines",
                          )
    else:
        money_details = ""
    time = raw["req_organisation_needs.vol"]
    if time:
        time_details = record["req_organisation_needs.vol_details"]
        time_details = P(I(_class="icon icon-time"),
                         " ",
                         XML(time_details),
                         _class="card_manylines",
                         )
    else:
        time_details = ""

    org_id = raw["org_organisation.id"]
    org_url = URL(c="org", f="organisation", args=[org_id, "profile"])
    if logo:
        logo = A(IMG(_src=URL(c="default", f="download", args=[logo]),
                     _class="media-object",
                     ),
                 _href=org_url,
                 _class="pull-left",
                 )
    else:
        logo = DIV(IMG(_class="media-object"),
                   _class="pull-left")

    permit = current.auth.s3_has_permission
    table = current.db.req_organisation_needs
    if permit("update", table, record_id=record_id):
        edit_btn = A(I(" ", _class="icon icon-edit"),
                     _href=URL(c="req", f="organisation_needs",
                               args=[record_id, "update.popup"],
                               vars={"refresh": list_id,
                                     "record": record_id}),
                     _class="s3_modal",
                     _title=current.response.s3.crud_strings.req_organisation_needs.title_update,
                     )
    else:
        edit_btn = ""
    if permit("delete", table, record_id=record_id):
        delete_btn = A(I(" ", _class="icon icon-trash"),
                       _class="dl-item-delete",
                      )
    else:
        delete_btn = ""
    edit_bar = DIV(edit_btn,
                   delete_btn,
                   _class="edit-bar fright",
                   )

    if current.request.controller == "org":
        # Org Profile page - no need to repeat Org Name
        title = " "
    else:
        title = raw["org_organisation.name"]

    # Render the item
    item = DIV(DIV(SPAN(title, _class="card-title"),
                   SPAN(author, _class="location-title"),
                   SPAN(date, _class="date-title"),
                   edit_bar,
                   _class="card-header",
                   ),
                   DIV(logo,
                       DIV(P(I(_class="icon icon-phone"),
                             " ",
                             phone,
                             _class="card_1_line",
                             ),
                           P(I(_class="icon icon-map"),
                             " ",
                             website,
                             _class="card_1_line",
                             ),
                           money_details,
                           time_details,
                           _class="media-body",
                           ),
                   _class="media",
                   ),
               _class=item_class,
               _id=item_id,
               )

    return item

s3.render_org_needs = render_org_needs

# -----------------------------------------------------------------------------
def render_site_needs(list_id, item_id, resource, rfields, record):
    """
        Custom dataList item renderer for Needs
        - UNUSED

        @param list_id: the HTML ID of the list
        @param item_id: the HTML ID of the item
        @param resource: the S3Resource to render
        @param rfields: the S3ResourceFields to render
        @param record: the record as dict
    """

    record_id = record["req_site_needs.id"]
    item_class = "thumbnail"

    raw = record._row
    logo = raw["org_organisation.logo"]
    addresses = raw["gis_location.addr_street"]
    if addresses:
        if isinstance(addresses, list):
            address = addresses[0]
        else:
            address = addresses
    else:
        address = ""
    #contact = raw["org_facility.contact"] or ""
    opening_times = raw["org_facility.opening_times"] or ""
    phone = raw["org_facility.phone1"] or ""
    website = raw["org_organisation.website"] or ""
    if website:
        website = A(website, _href=website)
    author = record["req_site_needs.modified_by"]
    date = record["req_site_needs.modified_on"]
    #goods = raw["req_site_needs.goods"]
    #if goods:
    #    goods_details = record["req_site_needs.goods_details"]
    #    goods_details = P(I(_class="icon icon-truck"),
    #                      " ",
    #                      XML(goods_details),
    #                      _class="card_1_line",
    #                      )
    #else:
    #    goods_details = ""
    #time = raw["req_site_needs.vol"]
    #if time:
    #    time_details = record["req_site_needs.vol_details"]
    #    time_details = P(I(_class="icon icon-time"),
    #                     " ",
    #                     XML(time_details),
    #                     _class="card_1_line",
    #                     )
    #else:
    #    time_details = ""

    site_url = URL(c="org", f="facility", args=[record_id, "profile"])
    if logo:
        logo = A(IMG(_src=URL(c="default", f="download", args=[logo]),
                     _class="media-object",
                     ),
                 _href=site_url,
                 _class="pull-left",
                 )
    else:
        logo = DIV(IMG(_class="media-object"),
                   _class="pull-left")

    permit = current.auth.s3_has_permission
    table = current.db.req_site_needs
    if permit("update", table, record_id=record_id):
        edit_btn = A(I(" ", _class="icon icon-edit"),
                     _href=URL(c="req", f="site_needs",
                               args=[record_id, "update.popup"],
                               vars={"refresh": list_id,
                                     "record": record_id}),
                     _class="s3_modal",
                     _title=current.response.s3.crud_strings.req_site_needs.title_update,
                     )
    else:
        edit_btn = ""
    if permit("delete", table, record_id=record_id):
        delete_btn = A(I(" ", _class="icon icon-trash"),
                       _class="dl-item-delete",
                      )
    else:
        delete_btn = ""
    edit_bar = DIV(edit_btn,
                   delete_btn,
                   _class="edit-bar fright",
                   )

    if current.request.controller == "org":
        # Site Profile page - no need to repeat Site Name
        title = " "
    else:
        title = raw["org_facility.name"]

    # Render the item
    item = DIV(DIV(SPAN(title, _class="card-title"),
                   SPAN(author, _class="location-title"),
                   SPAN(date, _class="date-title"),
                   edit_bar,
                   _class="card-header",
                   ),
               DIV(logo,
                   DIV(#goods_details,
                       #time_details,
                       P(I(_class="icon icon-home"),
                         " ",
                         address,
                         _class="card_manylines",
                         ),
                       P(I(_class="icon-time"),
                         " ",
                         SPAN(opening_times),
                         " ",
                         _class="card_1_line",
                         ),
                       P(I(_class="icon icon-phone"),
                         " ",
                         phone,
                         _class="card_1_line",
                         ),
                       P(I(_class="icon icon-map"),
                         " ",
                         website,
                         _class="card_1_line",
                         ),
                       P(I(_class="icon icon-user"),
                         " ",
                         contact,
                         _class="card_1_line",
                         ),
                       _class="media-body",
                       ),
                   _class="media",
                   ),
               _class=item_class,
               _id=item_id,
               )

    return item

s3.render_site_needs = render_site_needs

# =============================================================================
def hrm_shift_profile(r, **attr):
    """
        Custom Method for deployment page.
    """

    if r.http != "GET":
        r.error(405, current.ERROR.BAD_METHOD)

    db = current.db
    s3db = current.s3db
    output = {}
    record = r.record

    output["id"] = r.id
    output["event_id"] = r.record.event_id
    output["event"] = r.record.event_id.name
    output["human_resource"] = s3db.hrm_human_resource_represent(r.record.human_resource_id)
    output["start"] = r.record.start_datetime
    output["end"] = r.record.end_datetime

    #@ToDo: Edit the header information after edit

    # CMS Post Data List
    resource = s3db.resource("cms_post")
    resource.add_filter((FS("event.date") > record.start_datetime) & \
                        (FS("event.date") < record.end_datetime) & \
                        (FS("event_post.event_id") == record.event_id))
    list_id = "cms_newsfeed_datalist"
    list_fields = [#"series_id",
                   "location_id",
                   "date",
                   "body",
                   "created_by",
                   "created_by$organisation_id",
                   "document.file",
                   #"event_post.incident_id",
                   ]
    # Order with most recent Post first
    orderby = "cms_post.date desc"
    datalist, numrows, ids = resource.datalist(fields = list_fields,
                                               #start = None,
                                               limit = 10,
                                               list_id = list_id,
                                               orderby = orderby,
                                               layout = s3db.cms_post_list_layout,
                                               )
    ajax_url = URL(c="cms", f="post", args="datalist.dl", vars={"list_id": list_id})
    output[list_id] = datalist.html(ajaxurl = ajax_url,
                                    pagesize = 5
                                    )

    # Shift Human Resources Datalist
    resource = s3db.resource("hrm_shift_human_resource")
    resource.add_filter(FS("shift_human_resource.hrm_shift_id") == r.id)
    list_id = "hrm_shift_human_resource_datalist"
    datalist, numrows, ids = resource.datalist(#fields = list_fields,
                                               #start = None,
                                               limit = 10,
                                               list_id = list_id,
                                               #orderby = orderby,
                                               #layout = render_contacts,
                                               )
    ajax_url = URL(c="hrm", f="shift_human_resource", args="datalist.dl", vars={"list_id": list_id})
    output[list_id] = datalist.html(ajaxurl = ajax_url,
                                    pagesize = 5
                                    )

    # Set the custom view
    from os import path
    view = path.join(current.request.folder, "private", "templates",
                     "DERA", "views", "hrm_shift_profile.html")
    try:
        # Pass view as file not str to work in compiled mode
        current.response.view = open(view, "rb")
    except IOError:
        from gluon.http import HTTP
        raise HTTP(404, "Unable to open Custom View: %s" % view)

    return output

# -----------------------------------------------------------------------------
def customise_hrm_shift_controller(**attr):
    """
        Customise hrm_shift controller
        - Profile Page
        - Requests
    """
    s3db = current.s3db
    s3 = current.response.s3

    s3db.configure("hrm_shift",
                   create_next = URL(c="hrm",
                                     f="shift",
                                     args=["[id]",
                                           "profile"]),
                   )

    # Custom PreP
    standard_prep = s3.prep
    def custom_prep(r):
        # Call standard prep
        if callable(standard_prep):
            result = standard_prep(r)
            if not result:
                return False

        if r.interactive:
            if r.method == "profile":
                # Set a custom method for profile page
                s3db.set_method(r.controller,
                                r.function,
                                method = "profile",
                                action = hrm_shift_profile)
        return True
    s3.prep = custom_prep
    return attr

settings.customise_hrm_shift_controller = customise_hrm_shift_controller

# -----------------------------------------------------------------------------
def customise_hrm_shift_resource(r, tablename):
    

    s3 = current.response.s3

    # Custom postp
    standard_postp = s3.postp
    def custom_postp(r, output):
        # Call standard postp
        if callable(standard_postp):
            output = standard_postp(r, output)

        if r.interactive and isinstance(output, dict):
            actions = [dict(label=str(T("Open")),
                            _class="action-btn",
                            url=URL(c="hrm", f="shift",
                                    args=["[id]", "profile"])),
                       ]
            s3.actions = actions

        return output
    s3.postp = custom_postp

settings.customise_hrm_shift_resource = customise_hrm_shift_resource

# -----------------------------------------------------------------------------
def customise_event_incident_resource(r, tablename):

    s3db = current.s3db

    event_id = s3db.event_incident.event_id
    event_id.readable = True
    event_id.writable = True

    s3.crud_strings[tablename].title_list = T("Status Action Board")
    
    s3db.configure(tablename,
                   create_next = None,
                   )

settings.customise_event_incident_resource = customise_event_incident_resource

# -----------------------------------------------------------------------------
def customise_hrm_human_resource_fields():
    """
        Customise hrm_human_resource for Profile widgets and 'more' popups
    """

    s3db = current.s3db
    table = s3db.hrm_human_resource
    table.site_id.represent = S3Represent(lookup="org_site")
    s3db.org_site.location_id.represent = s3db.gis_LocationRepresent(sep=" | ")
    #table.modified_by.represent = s3_auth_user_represent_name
    table.modified_on.represent = datetime_represent

    list_fields = ["person_id",
                   "person_id$pe_id",
                   "organisation_id",
                   "site_id$location_id",
                   "site_id$location_id$addr_street",
                   "job_title_id",
                   "email.value",
                   "phone.value",
                   #"modified_by",
                   "modified_on",
                   ]

    s3db.configure("hrm_human_resource",
                   list_fields = list_fields,
                   )

# -----------------------------------------------------------------------------
def customise_hrm_human_resource_controller(**attr):
    """
        Customise hrm_human_resource controller
        - used for 'more' popups
    """

    s3 = current.response.s3

    # Custom PreP
    standard_prep = s3.prep
    def custom_prep(r):
        # Call standard prep
        if callable(standard_prep):
            result = standard_prep(r)
            if not result:
                return False

        if r.method == "datalist":
            customise_hrm_human_resource_fields()
            current.s3db.configure("hrm_human_resource",
                                   # Don't include a Create form in 'More' popups
                                   listadd = False,
                                   list_layout = render_contacts,
                                   )

        return True
    s3.prep = custom_prep

    return attr

settings.customise_hrm_human_resource_controller = customise_hrm_human_resource_controller

# -----------------------------------------------------------------------------
def customise_hrm_job_title_controller(**attr):

    s3 = current.response.s3

    table = current.s3db.hrm_job_title
    
    # Configure fields
    field = table.organisation_id
    field.readable = field.writable = False
    field.default = None
    
    # Custom postp
    standard_postp = s3.postp
    def custom_postp(r, output):
        if r.interactive:
            actions = [dict(label=str(T("Open")),
                            _class="action-btn",
                            url=URL(c="hrm", f="job_title",
                                    args=["[id]", "read"]))
                       ]
            db = current.db
            auth = current.auth
            has_permission = auth.s3_has_permission
            ownership_required = auth.permission.ownership_required
            s3_accessible_query = auth.s3_accessible_query
            if has_permission("update", table):
                action = dict(label=str(T("Edit")),
                              _class="action-btn",
                              url=URL(c="hrm", f="job_title",
                                      args=["[id]", "update"]),
                              )
                if ownership_required("update", table):
                    # Check which records can be updated
                    query = s3_accessible_query("update", table)
                    rows = db(query).select(table._id)
                    restrict = []
                    rappend = restrict.append
                    for row in rows:
                        row_id = row.get("id", None)
                        if row_id:
                            rappend(str(row_id))
                    action["restrict"] = restrict
                actions.append(action)
            if has_permission("delete", table):
                action = dict(label=str(T("Delete")),
                              _class="action-btn",
                              url=URL(c="hrm", f="job_title",
                                      args=["[id]", "delete"]),
                              )
                if ownership_required("delete", table):
                    # Check which records can be deleted
                    query = s3_accessible_query("delete", table)
                    rows = db(query).select(table._id)
                    restrict = []
                    rappend = restrict.append
                    for row in rows:
                        row_id = row.get("id", None)
                        if row_id:
                            rappend(str(row_id))
                    action["restrict"] = restrict
                actions.append(action)
            s3.actions = actions
            if isinstance(output, dict):
                if "form" in output:
                    output["form"].add_class("hrm_job_title")
                elif "item" in output and hasattr(output["item"], "add_class"):
                    output["item"].add_class("hrm_job_title")

        # Call standard postp
        if callable(standard_postp):
            output = standard_postp(r, output)

        return output
    s3.postp = custom_postp

    return attr

settings.customise_hrm_job_title_controller = customise_hrm_job_title_controller

# -----------------------------------------------------------------------------
def customise_org_organisation_controller(**attr):
    """
        Customise org_organisation controller
        - Profile Page
        - Requests
    """

    s3 = current.response.s3

    # Custom PreP
    standard_prep = s3.prep
    def custom_prep(r):
        # Call standard prep
        if callable(standard_prep):
            result = standard_prep(r)
            if not result:
                return False

        if r.interactive or r.representation == "aadata":
            # Load normal Model
            s3db = current.s3db
            table = s3db.org_organisation

            list_fields = ["id",
                           "name",
                           "logo",
                           "phone",
                           "website",
                           "needs.money",
                           "needs.money_details",
                           #"needs.vol",
                           #"needs.vol_details",
                           ]

            if r.method == "profile":
                # Customise tables used by widgets
                customise_hrm_human_resource_fields()
                #customise_org_facility_fields()
                #customise_org_needs_fields(profile=True)
                s3db.org_customise_org_resource_fields("profile")

                contacts_widget = dict(label = "Contacts",
                                       label_create = "Create Contact",
                                       type = "datalist",
                                       tablename = "hrm_human_resource",
                                       context = "organisation",
                                       create_controller = "pr",
                                       create_function = "person",
                                       icon = "icon-contact",
                                       show_on_map = False, # Since they will show within Offices
                                       list_layout = render_contacts,
                                       )
                map_widget = dict(label = "Map",
                                  type = "map",
                                  context = "organisation",
                                  icon = "icon-map",
                                  height = 383,
                                  width = 568,
                                  )
                needs_widget = dict(label = "Needs",
                                    label_create = "Add New Need",
                                    type = "datalist",
                                    tablename = "req_organisation_needs",
                                    multiple = False,
                                    context = "organisation",
                                    icon = "icon-hand-up",
                                    show_on_map = False,
                                    list_layout = render_org_needs,
                                    )
                reqs_widget = dict(label = "Requests",
                                   label_create = "Add New Request",
                                   type = "datalist",
                                   tablename = "req_req",
                                   context = "organisation",
                                   filter = FS("req_status").belongs([0, 1]),
                                   icon = "icon-flag",
                                   layer = "Requests",
                                   # provided by Catalogue Layer
                                   #marker = "request",
                                   list_layout = s3db.req_req_list_layout,
                                   )
                #resources_widget = dict(label = "Resources",
                #                        label_create = "Create Resource",
                #                        type = "datalist",
                #                        tablename = "org_resource",
                #                        context = "organisation",
                #                        #filter = FS("req_status").belongs([0, 1]),
                #                        icon = "icon-wrench",
                #                        layer = "Resources",
                #                        # provided by Catalogue Layer
                #                        #marker = "resource",
                #                        list_layout = s3db.org_resource_list_layout,
                #                        )
                commits_widget = dict(label = "Donations",
                                      #label_create = "Add New Donation",
                                      type = "datalist",
                                      tablename = "req_commit",
                                      context = "organisation",
                                      filter = FS("cancel") == False,
                                      icon = "icon-truck",
                                      show_on_map = False,
                                      #layer = "Donations",
                                      # provided by Catalogue Layer
                                      #marker = "donation",
                                      list_layout = s3db.req_commit_list_layout,
                                      )
                sites_widget = dict(label = "Sites",
                                    label_create = "Add New Site",
                                    type = "datalist",
                                    tablename = "org_facility",
                                    context = "organisation",
                                    filter = FS("obsolete") == False,
                                    icon = "icon-home",
                                    layer = "Facilities",
                                    # provided by Catalogue Layer
                                    #marker = "office",
                                    list_layout = render_sites,
                                    )
                record = r.record
                record_id = record.id
                if current.auth.s3_has_permission("update", table, record_id=record_id):
                    edit_btn = A(I(_class = "icon icon-edit"),
                                 _href=URL(c="org", f="organisation",
                                           args=[record_id, "update.popup"],
                                           vars={"refresh": "datalist"}),
                                 _class="s3_modal",
                                 _title=s3.crud_strings["org_organisation"].title_update,
                                 )
                else:
                    edit_btn = ""
                s3db.configure("org_organisation",
                               profile_title = "%s : %s" % (s3.crud_strings["org_organisation"].title_list, 
                                                            record.name),
                               profile_header = DIV(edit_btn,
                                                    IMG(_class="media-object",
                                                          _src=URL(c="default", f="download",
                                                                   args=[record.logo]),
                                                        ),
                                                    H2(record.name),
                                                    _class="profile-header",
                                                    ),
                               profile_widgets = [reqs_widget,
                                                  map_widget,
                                                  # @ToDo: Move to profile_header
                                                  #needs_widget,
                                                  #resources_widget,
                                                  commits_widget,
                                                  needs_widget,
                                                  contacts_widget,
                                                  sites_widget,
                                                  ]
                               )
            elif r.method == "datalist":
                # Stakeholder selection page
                # 2-column datalist, 6 rows per page
                s3.dl_pagelength = 12
                s3.dl_rowsize = 2

                from s3.s3filter import S3TextFilter, S3OptionsFilter
                filter_widgets = [
                    # no other filter widgets here yet?
                ]

                # Needs page
                # Truncate details field(s)
                from s3.s3utils import s3_trunk8
                s3_trunk8(lines=2)

                get_vars = current.request.get_vars
                money = get_vars.get("needs.money", None)
                #vol = get_vars.get("needs.vol", None)
                if money:
                    needs_fields = ["needs.money_details"]
                    s3.crud_strings["org_organisation"].title_list = T("Organizations soliciting Money")
                #elif vol:
                #    needs_fields = ["needs.vol_details"]
                #    s3.crud_strings["org_organisation"].title_list = T("Organizations with remote Volunteer opportunities")
                else:
                    yesno = {True: T("Yes"), False: T("No")}
                    needs_fields = ["needs.money_details", "needs.vol_details"]
                    filter_widgets.insert(0, S3OptionsFilter("needs.money",
                                                             options = yesno,
                                                             multiple = False,
                                                             cols = 2,
                                                             hidden = True,
                                                             ))
                    #filter_widgets.insert(1, S3OptionsFilter("needs.vol",
                    #                                         options = yesno,
                    #                                         multiple = False,
                    #                                         cols = 2,
                    #                                         hidden = True,
                    #                                         ))

                filter_widgets.insert(0, S3TextFilter(["name",
                                                       "acronym",
                                                       "website",
                                                       "comments",
                                                       ] + needs_fields,
                                                      label = T("Search")))

                ntable = s3db.req_organisation_needs
                s3db.configure("org_organisation",
                               filter_widgets = filter_widgets
                               )

            # Represent used in rendering
            current.auth.settings.table_user.organisation_id.represent = s3db.org_organisation_represent

            # Hide fields
            field = s3db.org_organisation_organisation_type.organisation_type_id
            field.readable = field.writable = False
            table.region_id.readable = table.region_id.writable = False
            table.country.readable = table.country.writable = False
            table.year.readable = table.year.writable = False
            
            # Return to List view after create/update/delete (unless done via Modal)
            url_next = URL(c="org", f="organisation", args="datalist")

            s3db.configure("org_organisation",
                           create_next = url_next,
                           delete_next = url_next,
                           update_next = url_next,
                           # We want the Create form to be in a modal, not inline, for consistency
                           listadd = False,
                           list_fields = list_fields,
                           list_layout = render_organisations,
                           )

        return True
    s3.prep = custom_prep

    # Custom postp
    standard_postp = s3.postp
    def custom_postp(r, output):
        if r.interactive and \
           isinstance(output, dict) and \
           current.auth.s3_has_permission("create", r.table):
            # Insert a Button to Create New in Modal
            output["showadd_btn"] = A(I(_class="icon icon-plus-sign big-add"),
                                      _href=URL(c="org", f="organisation",
                                                args=["create.popup"],
                                                vars={"refresh": "datalist"}),
                                      _class="btn btn-primary s3_modal",
                                      _role="button",
                                      _title=T("Create Organization"),
                                      )

        # Call standard postp
        if callable(standard_postp):
            output = standard_postp(r, output)

        return output
    s3.postp = custom_postp

    return attr

settings.customise_org_organisation_controller = customise_org_organisation_controller

# -----------------------------------------------------------------------------
def customise_pr_person_controller(**attr):

    s3db = current.s3db
    request = current.request
    s3 = current.response.s3

    tablename = "pr_person"
    table = s3db.pr_person

    # Custom PreP
    standard_prep = s3.prep
    def custom_prep(r):
        # Call standard prep
        if callable(standard_prep):
            result = standard_prep(r)
            if not result:
                return False

        if r.method == "validate":
            # Can't validate image without the file
            image_field = s3db.pr_image.image
            image_field.requires = None

        if r.interactive or r.representation == "aadata":
            if request.controller != "default":
                # CRUD Strings
                ADD_CONTACT = T("Create Contact")
                s3.crud_strings[tablename] = Storage(
                    label_create = T("Create Contact"),
                    title_display = T("Contact Details"),
                    title_list = T("Contact Directory"),
                    title_update = T("Edit Contact Details"),
                    label_list_button = T("List Contacts"),
                    label_delete_button = T("Delete Contact"),
                    msg_record_created = T("Contact added"),
                    msg_record_modified = T("Contact details updated"),
                    msg_record_deleted = T("Contact deleted"),
                    msg_list_empty = T("No Contacts currently registered"))

            MOBILE = settings.get_ui_label_mobile_phone()
            EMAIL = T("Email")

            htable = s3db.hrm_human_resource
            htable.organisation_id.widget = None
            site_field = htable.site_id
            represent = S3Represent(lookup="org_site")
            site_field.represent = represent
            site_field.requires = IS_ONE_OF(current.db, "org_site.site_id",
                                            represent,
                                            orderby = "org_site.name")
            from s3layouts import S3AddResourceLink
            site_field.comment = S3AddResourceLink(c="org", f="facility",
                                                   vars={"child": "site_id"},
                                                   label=T("Add New Site"),
                                                   title=T("Site"),
                                                   tooltip=T("If you don't see the Site in the list, you can add a new one by clicking link 'Add New Site'."))

            # ImageCrop widget doesn't currently work within an Inline Form
            s3db.pr_image.image.widget = None

            hr_fields = ["organisation_id",
                         "job_title_id",
                         "site_id",
                         "site_contact",
                         ]
            if r.method in ("create", "update"):
                # Context from a Profile page?"
                organisation_id = request.get_vars.get("(organisation)", None)
                if organisation_id:
                    field = s3db.hrm_human_resource.organisation_id
                    field.default = organisation_id
                    field.readable = field.writable = False
                    hr_fields.remove("organisation_id")

            s3_sql_custom_fields = [
                    "first_name",
                    #"middle_name",
                    "last_name",
                    S3SQLInlineComponent(
                        "human_resource",
                        name = "human_resource",
                        label = "",
                        multiple = False,
                        fields = hr_fields,
                    ),
                    S3SQLInlineComponent(
                        "image",
                        name = "image",
                        label = T("Photo"),
                        multiple = False,
                        fields = [("", "image")],
                        filterby = dict(field = "profile",
                                        options = [True]
                                        )
                    ),
                ]

            list_fields = [(current.messages.ORGANISATION, "human_resource.organisation_id"),
                           "first_name",
                           #"middle_name",
                           "last_name",
                           (T("Job Title"), "human_resource.job_title_id"),
                           (T("Site"), "human_resource.site_id"),
                           (T("Site Contact"), "human_resource.site_contact"),
                           ]

            # Don't include Email/Phone for unauthenticated users
            if current.auth.is_logged_in():
                list_fields += [(MOBILE, "phone.value"),
                                (EMAIL, "email.value"),
                                ]
                s3_sql_custom_fields.insert(3,
                                            S3SQLInlineComponent(
                                            "contact",
                                            name = "phone",
                                            label = MOBILE,
                                            multiple = False,
                                            fields = [("", "value")],
                                            filterby = dict(field = "contact_method",
                                                            options = "SMS")),
                                            )
                s3_sql_custom_fields.insert(3,
                                            S3SQLInlineComponent(
                                            "contact",
                                            name = "email",
                                            label = EMAIL,
                                            multiple = False,
                                            fields = [("", "value")],
                                            filterby = dict(field = "contact_method",
                                                            options = "EMAIL")),
                                            )

            crud_form = S3SQLCustomForm(*s3_sql_custom_fields)

            if r.id and request.controller == "default":
                url_next = URL(c="default", f="person", args=[r.id, "read"])
            else:
                # Return to List view after create/update/delete (unless done via Modal)
                url_next = URL(c="pr", f="person")

            s3db.configure(tablename,
                           create_next = url_next,
                           crud_form = crud_form,
                           delete_next = url_next,
                           list_fields = list_fields,
                           # Don't include a Create form in 'More' popups
                           listadd = False if r.method=="datalist" else True,
                           list_layout = render_contacts,
                           update_next = url_next,
                           )

            # Move fields to their desired Locations
            # Disabled as breaks submission of inline_component
            #i18n = []
            #iappend = i18n.append
            #iappend('''i18n.office="%s"''' % T("Office"))
            #iappend('''i18n.organisation="%s"''' % T("Organization"))
            #iappend('''i18n.job_title="%s"''' % T("Job Title"))
            #i18n = '''\n'''.join(i18n)
            #s3.js_global.append(i18n)
            #s3.scripts.append('/%s/static/themes/DRMP/js/contacts.js' % request.application)

        return True
    s3.prep = custom_prep

    # Custom postp
    standard_postp = s3.postp
    def custom_postp(r, output):
        # Call standard postp
        if callable(standard_postp):
            output = standard_postp(r, output)

        if r.interactive and isinstance(output, dict):
            output["rheader"] = ""
            actions = [dict(label=str(T("Open")),
                            _class="action-btn",
                            url=URL(c="pr", f="person",
                                    args=["[id]", "read"]))
                       ]
            # All users just get "Open"
            #db = current.db
            #auth = current.auth
            #has_permission = auth.s3_has_permission
            #ownership_required = auth.permission.ownership_required
            #s3_accessible_query = auth.s3_accessible_query
            #if has_permission("update", table):
            #    action = dict(label=str(T("Edit")),
            #                  _class="action-btn",
            #                  url=URL(c="pr", f="person",
            #                          args=["[id]", "update"]),
            #                  )
            #    if ownership_required("update", table):
            #        # Check which records can be updated
            #        query = s3_accessible_query("update", table)
            #        rows = db(query).select(table._id)
            #        restrict = []
            #        rappend = restrict.append
            #        for row in rows:
            #            row_id = row.get("id", None)
            #            if row_id:
            #                rappend(str(row_id))
            #        action["restrict"] = restrict
            #    actions.append(action)
            #if has_permission("delete", table):
            #    action = dict(label=str(T("Delete")),
            #                  _class="action-btn",
            #                  url=URL(c="pr", f="person",
            #                          args=["[id]", "delete"]),
            #                  )
            #    if ownership_required("delete", table):
            #        # Check which records can be deleted
            #        query = s3_accessible_query("delete", table)
            #        rows = db(query).select(table._id)
            #        restrict = []
            #        rappend = restrict.append
            #        for row in rows:
            #            row_id = row.get("id", None)
            #            if row_id:
            #                rappend(str(row_id))
            #        action["restrict"] = restrict
            #    actions.append(action)
            s3.actions = actions
            if "form" in output:
                output["form"].add_class("pr_person")
            elif "item" in output and hasattr(output["item"], "add_class"):
                output["item"].add_class("pr_person")

        return output
    #s3.postp = custom_postp

    return attr

#settings.customise_pr_person_controller = customise_pr_person_controller

# -----------------------------------------------------------------------------
def customise_doc_document_controller(**attr):

    s3 = current.response.s3
    s3db = current.s3db
    tablename = "doc_document"
    table = s3db.doc_document

    # Custom PreP
    standard_prep = s3.prep
    def custom_prep(r):
        # Call standard prep
        if callable(standard_prep):
            result = standard_prep(r)

        # Filter Out Docs from Newsfeed
        current.response.s3.filter = (table.name != None)

        if r.interactive:
            s3.crud_strings[tablename] = Storage(
                label_create = T("Add Document"),
                title_display = T("Document"),
                title_list = T("Documents"),
                title_update = T("Edit Document"),
                label_list_button = T("List New Documents"),
                label_delete_button = T("Remove Documents"),
                msg_record_created = T("Documents added"),
                msg_record_modified = T("Documents updated"),
                msg_record_deleted = T("Documents removed"),
                msg_list_empty = T("No Documents currently recorded"))

            # Force added docs to have a name
            table.name.requires = IS_NOT_EMPTY()

            list_fields = ["name",
                           "file",
                           "url",
                           "organisation_id",
                           "comments",
                           ]

            crud_form = S3SQLCustomForm(*list_fields)

            s3db.configure(tablename,
                           list_fields = list_fields,
                           crud_form = crud_form,
                           )
        return True
    s3.prep = custom_prep

    return attr

settings.customise_doc_document_controller = customise_doc_document_controller

# =============================================================================
# Modules
# Comment/uncomment modules here to disable/enable them
settings.modules = OrderedDict([
    # Core modules which shouldn't be disabled
    ("default", Storage(
        name_nice = "Home",
        restricted = False, # Use ACLs to control access to this module
        access = None,      # All Users (inc Anonymous) can see this module in the default menu & access the controller
        module_type = None  # This item is not shown in the menu
    )),
    ("admin", Storage(
        name_nice = "Administration",
        #description = "Site Administration",
        restricted = True,
        access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
        module_type = None  # This item is handled separately for the menu
    )),
    ("appadmin", Storage(
        name_nice = "Administration",
        #description = "Site Administration",
        restricted = True,
        module_type = None  # No Menu
    )),
    ("errors", Storage(
        name_nice = "Ticket Viewer",
        #description = "Needed for Breadcrumbs",
        restricted = False,
        module_type = None  # No Menu
    )),
    ("sync", Storage(
        name_nice = "Synchronization",
        #description = "Synchronization",
        restricted = True,
        access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
        module_type = None  # This item is handled separately for the menu
    )),
    ("translate", Storage(
        name_nice = "Translation Functionality",
        #description = "Selective translation of strings based on module.",
        module_type = None,
    )),
    ("gis", Storage(
        name_nice = "Map",
        #description = "Situation Awareness & Geospatial Analysis",
        restricted = True,
        module_type = 1,     # 1st item in the menu
    )),
    ("pr", Storage(
        name_nice = "Persons",
        #description = "Central point to record details on People",
        restricted = True,
        access = "|1|",     # Only Administrators can see this module in the default menu (access to controller is possible to all still)
        module_type = None
    )),
    ("org", Storage(
        name_nice = "Organizations",
        #description = 'Lists "who is doing what & where". Allows relief agencies to coordinate their activities',
        restricted = True,
        module_type = None
    )),
    # All modules below here should be possible to disable safely
    ("hrm", Storage(
        name_nice = "Contacts",
        #description = "Human Resources Management",
        restricted = True,
        module_type = None,
    )),
    ("cms", Storage(
            name_nice = "Content Management",
            restricted = True,
            module_type = None,
        )),
    ("doc", Storage(
        name_nice = "Documents",
        #description = "A library of digital resources, such as photos, documents and reports",
        restricted = True,
        module_type = None,
    )),
    ("msg", Storage(
        name_nice = "Messaging",
        #description = "Sends & Receives Alerts via Email & SMS",
        restricted = True,
        # The user-visible functionality of this module isn't normally required. Rather it's main purpose is to be accessed from other modules.
        module_type = None,
    )),
    ("event", Storage(
        name_nice = "Disasters",
        #description = "Events",
        restricted = True,
        module_type = None
    )),
    ("req", Storage(
            name_nice = "Requests",
            #description = "Manage requests for supplies, assets, staff or other resources. Matches against Inventories where supplies are requested.",
            restricted = True,
            module_type = None,
        )),
    #("project", Storage(
    #    name_nice = "Projects",
    #    restricted = True,
    #    module_type = None
    #)),
    ("stats", Storage(
        name_nice = "Statistics",
        restricted = True,
        module_type = None
    )),
    #("vulnerability", Storage(
    #    name_nice = "Vulnerability",
    #    restricted = True,
    #    module_type = None
    #)),
    #("transport", Storage(
    #    name_nice = "Transport",
    #    restricted = True,
    #    module_type = None
    #)),
    #("hms", Storage(
    #    name_nice = "Hospitals",
    #    restricted = True,
    #    module_type = None
    #)),
    ("cr", Storage(
        name_nice = "Shelters",
        restricted = True,
        module_type = None
    )),
    ("supply", Storage(
        name_nice = "Supply Chain Management",
        restricted = True,
        module_type = None
    )),
])
