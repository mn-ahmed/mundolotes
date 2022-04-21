from odoo import _, api, fields, tools, models
from odoo.exceptions import UserError, ValidationError

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    is_lot_from_production = fields.Boolean(
        string='Is LOT From Production Warehouse',
        compute='compute_is_lot_from_production',
    )

    @api.depends('location_id', 'location_id.warehouse_id', 'location_id.warehouse_id.is_production_warehouse')
    def compute_is_lot_from_production(self):
        for record in self:
            if record.location_id and record.location_id.warehouse_id:
                record.is_lot_from_production = record.location_id.warehouse_id.is_production_warehouse
            else:
                record.is_lot_from_production = False

    def _compute_product_stock_quant_ids(self):
        res = super(StockMoveLine, self)._compute_product_stock_quant_ids()
        # for line in self:
            # line.product_stock_quant_ids = line.product_stock_quant_ids.filtered(lambda r: r.quantity > 20)
        if not self.is_lot_from_production:
            self.lot_id = False

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        if not self.is_lot_from_production:
            lot_stock_quant_ids = self.product_stock_quant_ids.filtered(lambda r: r.lot_id.name == self.lot_id.name)
            if lot_stock_quant_ids:
                self.qty_done = lot_stock_quant_ids[0].quantity
            else:
                self.qty_done = 0