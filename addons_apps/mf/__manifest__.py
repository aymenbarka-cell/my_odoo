{
        'name': 'MF Module test',
        'description': 'rien pour le moment',
        'depends': ['contacts','hr','stock','sale'],

        'data': [
            "security/security.xml",
            "security/ir.model.access.csv",
            "data/res_partner.xml",
            "views/formation_salle.xml" ,
            "views/formation_type.xml",
            "views/formation_formation.xml",
            "views/res_partner_view.xml",
            "views/sale_order_view.xml",
            "views/stock_picking_view.xml",
            "views/hr_employee_view.xml",
            "views/sequence.xml",
            "report/formation_salle_report.xml",
            # "views/formation_report.xml",
            ],

}