{
    'name': 'Project Management',
    'author':'Khaled GP',
    'version': '1.0',
    'category': '',
    'depends': ['base','hr','mail','calendar'],
    'data': [
        'views/calendar_event_attendees.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/project_management_view.xml',
        'reports/project_management_reports.xml'

    ],
    'application': True,
    'installable': True,
}
