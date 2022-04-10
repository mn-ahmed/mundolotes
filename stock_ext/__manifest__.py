{
    'name': "Inventory (Extension)",
    'summary': "Custom App/Extension in Inventory App.",
    'author': 'Numan Umer',
    'company': 'Numan Umer',
    'website': 'https://www.linkedin.com/in/numanumer/',
    'sequence': 25,
    'version': '15.0.1.0.0',
    'category': 'Inventory/Inventory',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [

        'report/report_deliveryslip_summarized.xml',
        'report/stock_report_views.xml',

        'views/product_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_move_views.xml',
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
