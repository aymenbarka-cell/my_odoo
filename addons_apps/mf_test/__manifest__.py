
{
    "name": "module MF formation",
    'description': """ 
    Module pour apprendre a programmer dans odoo
    """,
    "depends": ['contacts','hr','sale_stock'],
    "data": [
        'security/formation_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',

        'views/formation_salle.xml',
        'views/formation_type.xml',
        'views/formation_formation.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/hr_employee_view.xml',

        'wizard/formation_report.xml',

        'report/formation_salle_report.xml',
        'report/formation_report.xml',
    ],
}
