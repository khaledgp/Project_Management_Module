from odoo import models, fields, api


class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    activity_user_id = fields.Many2one('res.users', string='Activity User')
    activity_ids = fields.One2many('mail.activity', 'res_id', domain=[('res_model', '=', 'project.task')],
                                   string='Scheduled Activities')

    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)

        assigned_employee = task.assigned_to
        assigned_user = assigned_employee.user_id or self.env.user

        self._create_or_update_activity(task, assigned_user)

        return task

    def write(self, vals):
        for task in self:
            if 'assigned_to' in vals or 'due_date' in vals:
                if 'assigned_to' in vals:
                    assigned_employee = vals.get('assigned_to')
                    if assigned_employee:
                        assigned_employee = self.env['hr.employee'].browse(assigned_employee)

                    assigned_user = assigned_employee.user_id or self.env.user

                else:
                    assigned_user = task.assigned_to.user_id or self.env.user

                due_date = vals.get('due_date')

                self._create_or_update_activity(task, assigned_user, due_date)

        return super(ProjectTask, self).write(vals)

    def _create_or_update_activity(self, task, assigned_user, due_date=None):
        task_model_id = self.env['ir.model'].search([('model', '=', 'project.task')], limit=1).id

        if not due_date:
            due_date = task.due_date

        activity = task.activity_ids.filtered(lambda a: a.activity_type_id.id ==  self.env.ref('mail.mail_activity_data_todo').id)

        values = {
            'display_name': task.name,
            'summary': task.description,
            'date_deadline': due_date,
            'user_id': assigned_user.id if assigned_user.id else self.env.user,
            'res_id': task.id,
            'res_model_id': task_model_id,
            'activity_type_id':  self.env.ref('mail.mail_activity_data_todo').id,
        }

        if activity:
            activity.write(values)
        else:
            self.env['mail.activity'].create(values)


