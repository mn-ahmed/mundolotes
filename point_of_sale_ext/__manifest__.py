# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Orders Analysis Extension',
    'version': '1.0.1',
    'category': 'Sales/Point of Sale',
    'sequence': 40,
    'summary': 'Orders Analysis Extension',
    'description': "",
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_order_report_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'website': 'https://www.odoo.com/app/point-of-sale-shop',
    'license': 'LGPL-3',
}
