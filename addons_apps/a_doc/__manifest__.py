{
    'name': 'Document Archive',
    'version': '1.0',
    'category': 'Document Management',
    'summary': 'Archive documents with hierarchical structure',
    'description': """
        Archive documents under Company → Direction → Department → Section → Desk.
    """,
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/document_security.xml',
        'views/company_direction_views.xml',
        'views/department_views.xml',
        'views/section_views.xml',
        'views/desk_views.xml',
        'views/document_views.xml',
        'views/menu.xml',
        'views/document_category_views.xml',  
        'views/document_tag_views.xml',
        'views/user_views.xml', 
    ],
    'installable': True,
    'application': True,
}