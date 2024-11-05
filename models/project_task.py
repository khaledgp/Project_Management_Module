from odoo import models, fields

class ProjectManagement(models.Model):
    _name = 'project.task'

    name = fields.Char(string='Task Name', required=True)
    project_id = fields.Many2one('project.management', string='Project', required=True)
    description = fields.Text(string='Description')
    assigned_to = fields.Many2one('hr.employee', string='Assigned To', required=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='low')

    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Task Status', default='to_do')

    progress = fields.Float(string='Progress', default=0.0)
    due_date = fields.Date(string='Due Date')
    date_start = fields.Date(string='Start Date')