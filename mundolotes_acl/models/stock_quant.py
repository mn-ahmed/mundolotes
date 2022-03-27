
from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    warehouse_id = fields.Many2one(
        string='Warehouse',
        comodel_name='stock.warehouse',
        related='location_id.warehouse_id'
    )
    