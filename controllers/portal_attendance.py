from odoo import fields, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError
from odoo.http import request


class SisAttendancePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        AttendanceLog = request.env["sis.student.attendance.log"]
        partner = request.env.user.partner_id
        domain = [("enrollment_id.partner_id", "=", partner.id)]

        if "attendance_count" in counters:
            values["attendance_count"] = AttendanceLog.sudo().search_count(domain)

        if "attendance_unseen_count" in counters:
            values["attendance_unseen_count"] = AttendanceLog.sudo().search_count(
                domain + [("is_parent_seen", "=", False)]
            )

        return values

    @http.route(["/my", "/my/home"], type="http", auth="user", website=True)
    def portal_my_home(self, **kwargs):
        values = self._prepare_home_portal_values(
            ["enrollment_count", "attendance_count", "attendance_unseen_count"]
        )
        return request.render("portal.portal_my_home", values)

    @http.route(["/my/attendance"], type="http", auth="user", website=True)
    def portal_my_attendance(self, filterby="all", **kwargs):
        partner = request.env.user.partner_id
        AttendanceLog = request.env["sis.student.attendance.log"].sudo()

        domain = [("enrollment_id.partner_id", "=", partner.id)]
        today = fields.Date.context_today(request.env.user)
        searchbar_filters = {
            "all": {"label": "All", "domain": []},
            "unseen": {"label": "New", "domain": [("is_parent_seen", "=", False)]},
            "today": {"label": "Today", "domain": [("attendance_date", "=", today)]},
        }
        filterby = filterby if filterby in searchbar_filters else "all"
        domain += searchbar_filters[filterby]["domain"]

        attendance_logs = AttendanceLog.search(domain, order="attendance_datetime desc, id desc")

        return request.render(
            "obbs_sis_parent_attendance_portal.portal_attendance_list",
            {
                "attendance_logs": attendance_logs,
                "page_name": "attendance",
                "default_url": "/my/attendance",
                "searchbar_filters": searchbar_filters,
                "filterby": filterby,
            },
        )

    @http.route(
        ["/my/attendance/<int:attendance_log_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_attendance_page(self, attendance_log_id, **kwargs):
        attendance_log = request.env["sis.student.attendance.log"].sudo().browse(attendance_log_id)
        if not attendance_log.exists():
            return request.redirect("/my/attendance")

        partner = request.env.user.partner_id
        if attendance_log.enrollment_id.partner_id != partner and not request.env.user.has_group(
            "base.group_system"
        ):
            raise AccessError("You don't have access to this attendance log.")

        if not attendance_log.is_parent_seen:
            attendance_log.sudo().write(
                {
                    "is_parent_seen": True,
                    "parent_seen_datetime": attendance_log._portal_now(),
                }
            )

        return request.render(
            "obbs_sis_parent_attendance_portal.portal_attendance_page",
            {
                "attendance_log": attendance_log,
                "page_name": "attendance_detail",
            },
        )
