
from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_categ_id = fields.Many2one(related='product_tmpl_id.categ_id', store=True,)
    
    product_default_code = fields.Char(
        string='Internal Reference',
        related='product_tmpl_id.default_code',
        store=True,
    )
    