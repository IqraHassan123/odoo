{
    'name': 'Assets Management',
    'version': '1.0',
    'depends': [
        'base',
        'hr',
        'base_setup',
    ],
    'author': 'Author Name',
    'category': 'OMS/Assets',
    'summary': 'Module to manage assets with custom settings integration.',
    'description': """
        This module provides functionality to manage assets with customizable settings 
        accessible through the general settings menu.
    """,
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/category_views.xml",
        "views/attributes.xml",
        "views/asset_handling_views.xml",
        "views/asset_file.xml",
        "views/menus.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'GPL-2',
}
