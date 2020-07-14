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
        'mail'
    ],
    'data': [
        'views/patient.xml',
        'security/ir.model.access.csv'
    ],
    #'demo': [''],
    'installable': True,
    'application': True,
    'sequence': '5',
    'auto_install': False,
}