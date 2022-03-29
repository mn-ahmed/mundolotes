from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_warehouse_ids = fields.Many2many(
        string='Allowed Warehouses',
        comodel_name='stock.warehouse',
        relation='res_users_stock_warehouse_rel',
        column1='user_id',
        column2='warehouse_id',
    )
    
    @api.onchange('allowed_warehouse_ids')
    def onchange_allowed_warehouse_ids(self):
        self.clear_caches()
