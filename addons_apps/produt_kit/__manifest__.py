{
    'name': 'Product Kit',
    'version': '1.0',
    'category': 'Product',
    'summary': 'Manage product kits composed of existing products',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_kit_views.xml',
    ],
    'installable': True,
    'application': False,
}
