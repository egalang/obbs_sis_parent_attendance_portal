from odoo import api, fields, models


class StudentAttendanceLog(models.Model):
    _inherit = "sis.student.attendance.log"

    is_parent_seen = fields.Boolean(
        string="Seen by Parent",
        default=False,
        copy=False,
        help="Checked when the related portal parent has opened this attendance log.",
    )
    parent_seen_datetime = fields.Datetime(
        string="Parent Seen Datetime",
        copy=False,
        help="Date and time when the related portal parent first opened this attendance log.",
    )
    attendance_date = fields.Date(
        string="Attendance Date",
        compute="_compute_attendance_date",
        store=True,
        index=True,
        help="Convenience field used for portal filtering by date.",
    )

    @api.depends("attendance_datetime")
    def _compute_attendance_date(self):
        for record in self:
            record.attendance_date = (
                fields.Datetime.to_datetime(record.attendance_datetime).date()
                if record.attendance_datetime
                else False
            )

    def _portal_now(self):
        return fields.Datetime.now()
