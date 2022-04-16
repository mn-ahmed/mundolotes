from odoo import _, _lt, api, fields, models
from odoo.exceptions import UserError

class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    is_production_warehouse = fields.Boolean(
        string='Is Production Warehouse',
    )
    
