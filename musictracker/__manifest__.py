# -*- coding: utf-8 -*-
{
    'name': "MusicTracker",

    'summary': """
        Explora la música que te inspira""",

    'description': """
        Con este módulo podrán guardarse las valoraciones y reviews de una gran cantidad de usuarios 
        respecto a producciones musicales a nivel global y establecerles una nota media, así como 
        consultar varios detalles respecto a ellas.
    """,

    'author': "Robyn Navarro Gómez",
    'website': "https://github.com/robynngGH",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web', 'base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/star_rating_widget.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # css de FontAwesome para el widget de ratings
    'css': [
        'static/src/lib/fontawesome/css/all.css',
        'static/src/css/estilos_kanban.css',
    ],
    'installable': True,
    'application': True,
}
