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

        assigned_user = task.assigned_to.user_id if task.assigned_to and task.assigned_to.user_id else self.env.user

        task_model_id = self.env['ir.model'].search([('model', '=', 'project.task')], limit=1).id

        # check if the activity already exists
        activity = self.env['mail.activity'].search([('res_id', '=', task.id), ('activity_type_id', '=', 4)])

        # if the activity exists, update it
        if activity:
            activity.write({
                'display_name': task.name,
                'summary': 'test',
                'date_deadline': task.due_date,
                'user_id': assigned_user.user_id.id if assigned_user.user_id else self.env.user.id,
            })
        # if the activity does not exist, create it
        else:
            self.env['mail.activity'].create({
                'display_name': task.name,
                'summary': 'test',
                'date_deadline': task.due_date,
                'user_id': assigned_user.user_id.id if assigned_user.user_id else self.env.user.id,
                'res_id': task.id,
                'res_model_id': task_model_id,
                'activity_type_id': 4
            })

        #     if task.date_start and task.date_start > date.today():
        #     self.env['mail.activity'].create({
        #         'res_model': 'project.task',
        #         'res_model_id': task_model_id,
        #         'res_id': task.id,
        #         'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
        #         'user_id': assigned_user.user_id.id if assigned_user.user_id else self.env.user.id,
        #         'note': 'Task is starting soon, follow up!'
        #     })
        #
        # if task.due_date and task.due_date < date.today():
        #     self.env['mail.activity'].create({
        #         'res_model': 'project.task',
        #         'res_model_id': task_model_id,
        #         'res_id': task.id,
        #         'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
        #         'user_id': assigned_user.user_id.id if assigned_user.user_id else self.env.user.id,
        #         'note': 'Task is overdue, review required!'
        #     })

            task.activity_ids = task.activity_ids

        return task

    @api.onchange('status')
    def _onchange_task_status(self):
        if self.status == 'done':
            for activity in self.activity_ids:
                activity.write({'state': 'done'})
