# -*- coding: utf-8 -*-
{
    "name": "OBBS SIS Parent Attendance Portal",
    "summary": "Parent portal attendance feed and unread tracking for OBBS SIS",
    "description": """
Adds a parent-facing attendance portal on top of obbs_sis.
- Portal attendance list and detail pages
- Unread/new attendance tracking for parents
- Portal home counters for attendance updates
    """,
    "author": "OBBS Co.",
    "website": "https://obbsco.com",
    "category": "Education",
    "version": "18.0.1.0.0",
    "depends": ["obbs_sis", "portal", "website"],
    "data": [
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "views/portal_attendance_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'obbs_sis_parent_attendance_portal/static/src/css/portal_attendance.css',
        ],
    },
    "installable": True,
    "application": False,
}
