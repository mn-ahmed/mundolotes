
from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_categ_id = fields.Many2one(related='product_id.categ_id', store=True,)
    
    product_default_code = fields.Char(
        string='Internal Reference',
        related='product_id.default_code',
        store=True,
    )
    product_barcode = fields.Char(
        string='Barcode',
        related='product_id.barcode',
        store=True,
    )

    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        related='product_id.currency_id'
    )
    
    product_list_price = fields.Float(
        string='Product Sales Price',
        related='product_id.list_price',
    )