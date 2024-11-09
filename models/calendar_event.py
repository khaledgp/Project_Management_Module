from odoo import models, fields


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    audience_ids = fields.Many2many(
        'hr.employee',
        'calendar_event_attendee_rel',
        'event_id',
        'employee_id',
        string='Attendees'
    )
