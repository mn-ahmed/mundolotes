# -*- coding: utf-8 -*-
{
    "name": "Alphabot POS",
    'summary': 'Impresora fiscal en Panamá',
    'description': 'Ajustes para usar Alphabot, y conectar Odoo con las impresoras fiscales',
    'author': 'AlphaPos',
    'website': 'http://alphapos.biz',
    "support": "info@alphapos.biz",
    "license": "Other proprietary",
    'category': 'Point of Sale',
    'sequence': 10,
    'version': '0.15.23.04.08',
    'depends': ['base','account','point_of_sale','alphabot_invoicing','pos_restaurant'],

    'data': [   
        'security/ir.model.access.csv',
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'alphabot_pos/static/src/js/*',
        ],
    },    

    'installable': True,
    'application': True,

  #  'images': ['static/description/banner.png'],
}
