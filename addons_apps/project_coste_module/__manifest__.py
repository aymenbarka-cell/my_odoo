{
    'name': 'Project Cost Estimate with Catalog',
    'version': '1.0',
    'summary': 'Project cost estimates + product catalog and templates',
    'category': 'Project',
    'author': 'You',
    'depends': ['project', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_cost_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
