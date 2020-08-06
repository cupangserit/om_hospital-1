{
    'name': 'Hospital Management',
    'version': '12.0.1.0.0',
    'summary': 'Module for Manage Hospital',
    'description': """ 
    Feature Module \n
        - Manage Hospital 
        - Manage Patient 
        - Manage doktor 
        - Manage Lab 
        - Manage Pharmacy 
        - Manage Appointment
    """,
    'category': 'Extra Tools',
    'author': 'LobotIjo',
    'maintainer':'AdesDev',
    'website': 'digitalfarmer.github.io',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'snailmail_account',
        'report_xlsx',
        'board',
        'sale',
        'muk_web_searchpanel',
        'web_notify'
    ],
    'data': [
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/template.xml',
        'views/settings.xml',
        'views/sale_order.xml',
        'views/dashboard.xml',
        'views/server_action.xml',
        'reports/report.xml',
        'reports/appointment.xml',
        'reports/patient_card.xml',
        'reports/sale_order_inherit.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/data.xml',
        'data/cron.xml',
        'data/mail_template.xml'

    ],
    #'demo': [''],
    'installable': True,
    'application': True,
    'sequence': '5',
    'auto_install': False,

}