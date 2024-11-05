from odoo import models, fields, api

from datetime import date


class ProjectManagement(models.Model):
    _name = 'project.management'

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold')
    ], string='Status', default='planning')
    assigned_team = fields.Many2one('hr.employee', string='Assigned Team', required=True)

    task_ids = fields.One2many('project.task', 'project_id', string='Tasks')

    total_tasks = fields.Integer(string='Total Tasks', compute='_compute_total_tasks')
    completed_tasks = fields.Integer(string='Completed Tasks', compute='_compute_completed_tasks')
    overdue_tasks = fields.Integer(string='Overdue Tasks', compute='_compute_overdue_tasks')

    @api.depends('task_ids')
    def _compute_total_tasks(self):
        for project in self:
            project.total_tasks = len(project.task_ids)

    @api.depends('task_ids.status')
    def _compute_completed_tasks(self):
        for project in self:
            project.completed_tasks = len([task for task in project.task_ids if task.status == 'done'])

    @api.depends('task_ids.due_date', 'task_ids.status')
    def _compute_overdue_tasks(self):
        today = date.today()
        for project in self:
            project.overdue_tasks = len([task for task in project.task_ids if
                                         task.due_date and task.due_date < today and task.status != 'done'])




