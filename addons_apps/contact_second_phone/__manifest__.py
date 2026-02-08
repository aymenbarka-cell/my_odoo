{
    'name': 'Contact Second Phone',
    'version': '18.0.1.0.0',
    'summary': 'Add a second phone number field to contacts',
    'description': 'This module adds a new field "Second Phone Number" to the Contacts module.',
    'author': 'Aymen Barkat',
    'depends': ['contacts'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
