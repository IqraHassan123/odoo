{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Author Name',
    'category': 'Real Estate',
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag.xml",
        "views/estate_type_menus.xml",
        "views/estate_menus.xml",
    ],
    'description': """
        This module allows you to manage real estate properties.
    """,
    'installable': True,
    'license': 'GPL-2',
}
