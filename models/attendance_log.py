from odoo import api, fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

FASTAPI_URL = "http://158.51.126.165:8002/api/v1/notify/attendance"
API_KEY = "your-secret-key"  # add this


class StudentAttendanceLog(models.Model):
    _inherit = "sis.student.attendance.log"

    is_parent_seen = fields.Boolean(default=False, copy=False)
    parent_seen_datetime = fields.Datetime(copy=False)

    attendance_date = fields.Date(
        compute="_compute_attendance_date",
        store=True,
        index=True,
    )

    @api.depends("attendance_datetime")
    def _compute_attendance_date(self):
        for record in self:
            record.attendance_date = (
                fields.Datetime.to_datetime(record.attendance_datetime).date()
                if record.attendance_datetime
                else False
            )

    # =========================
    # NOTIFICATION
    # =========================

    def _send_attendance_notification(self):
        for rec in self:
            try:
                # Skip already notified (correct behavior)
                if rec.is_notified:
                    continue

                # Resolve student
                enrollment = rec.enrollment_id
                if not enrollment or not enrollment.id:
                    continue

                student = enrollment.id
                parent = enrollment.partner_id

                if not parent:
                    continue

                # Filter log type
                if rec.log_type not in ["school_in", "school_out"]:
                    continue

                dt = rec.attendance_datetime

                if dt:
                    dt = fields.Datetime.context_timestamp(rec, dt)

                payload = {
                    "partner_id": parent.id,
                    "student_name": enrollment.display_name,
                    "log_type": rec.log_type.replace("_", " ").title(),
                    "time": dt.strftime("%I:%M %p") if dt else ""
                }

                response = requests.post(
                    FASTAPI_URL,
                    json=payload,
                    headers={"X-API-Key": API_KEY},
                    timeout=3
                )

                if response.status_code == 200:
                    # ✅ Mark ONLY on success
                    rec.sudo().write({"is_notified": True})
                else:
                    _logger.warning(f"Notification failed: {response.text}")

            except Exception as e:
                _logger.error(f"Notification error: {e}")

    # =========================
    # CREATE
    # =========================

    @api.model
    def create(self, vals):
        record = super().create(vals)

        def notify():
            try:
                record.sudo()._send_attendance_notification()
            except Exception as e:
                _logger.error(f"Async notification failed: {e}")

        # Run ONLY after transaction is committed
        self.env.cr.postcommit.add(notify)

        return record

    def _portal_now(self):
        return fields.Datetime.now()