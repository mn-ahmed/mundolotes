{
    'name': "Barcode (Extension)",
    'summary': "Custom App/Extension in Barcode App.",
    'author': 'Numan Umer',
    'company': 'Numan Umer',
    'website': 'https://www.linkedin.com/in/numanumer/',
    'sequence': 255,
    'version': '15.0.1.0.0',
    'category': 'Inventory/Inventory',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'stock_barcode',
    ],
    'data': [
        'views/stock_warehouse_views.xml',
        'views/stock_move_line_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'external_dependencies': {
        'python': [
        ],
    }
}
