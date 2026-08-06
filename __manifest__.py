{
    'name': "Library Management",
    'version': '19.0.1.0.0',
    'summary': "Manage books and borrowers",
    'description': """
        A simple library/book management module for internal learning purposes.
    """,
    'author': "Raksmey",
    'license': "LGPL-3",
    'category': 'Productivity',
    'depends': ['base'],    
    'data': [
        'security/ir.model.access.csv',
        'views/library_menus.xml',
        'views/library_borrow_wizard_views.xml',
        'views/library_book_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}