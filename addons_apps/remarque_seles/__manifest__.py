{
    'name': 'Sale Order Remarque',
    'version': '1.0',
    'summary': 'Add a Remarque (remark/note) page to quotations and sales orders',
    'description': """
This module adds a new "Remarque" tab in the quotation/sale order form
to allow users to add internal notes or remarks.
    """,
    'author': 'Your Name',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'views/ajoute.xml',
        'views/ajoute_bd.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
