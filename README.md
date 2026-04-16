# OBBS SIS Parent Attendance Portal

A lightweight Odoo addon that provides a **parent-facing attendance portal** for the OBBS Student Information System (`obbs_sis`).

This module replaces email-based notifications with a **portal-based attendance feed** featuring **unread tracking**, allowing parents to view student attendance updates directly in the portal.

---

## 🚀 Features

- 📋 **Parent Attendance Portal**
  - Accessible via `/my/attendance`
  - Displays attendance logs مرتبط with the parent’s student(s)

- 🔔 **Unread / Seen Tracking**
  - New attendance logs are marked as **New**
  - Automatically marked as **Seen** when opened

- 👨‍👩‍👧 **Secure Access**
  - Parents can only view attendance logs مرتبط to their own children
  - Uses `sis.enrollment.partner_id` for filtering

- 🧩 **Seamless Integration**
  - Fully depends on `obbs_sis`
  - No changes required in the core module

- ❌ **No Email / No Chat**
  - Designed to replace email subscription
  - No chatter/discuss dependency

---

## 📦 Module Information

- **Module Name:** `obbs_sis_parent_attendance_portal`
- **Depends:** `obbs_sis`, `portal`
- **License:** LGPL-3

---

## ⚙️ Installation

1. Copy the module into your Odoo custom addons directory:

   ```bash
   /path/to/odoo/custom_addons/obbs_sis_parent_attendance_portal
