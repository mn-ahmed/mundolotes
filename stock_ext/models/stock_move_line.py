from odoo import _, api, fields, tools, models
from odoo.exceptions import UserError, ValidationError

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_categ_id = fields.Many2one(
        string='Product Category',
        comodel_name='product.category',
        related='product_id.categ_id',
        store=True,
    )
    product_id_default_code = fields.Char(
        string='Internal Reference',
        related='product_id.default_code',
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