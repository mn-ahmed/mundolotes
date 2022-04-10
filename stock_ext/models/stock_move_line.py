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
    
    qty_done_amount = fields.Float(
        string='Amount',
        compute='compute_qty_done_amount',
        store=True,
    )
        
    @api.depends('qty_done', 'product_list_price')
    def compute_qty_done_amount(self):
        for record in self:
            record.qty_done_amount = round(record.qty_done * record.product_list_price, 2)
