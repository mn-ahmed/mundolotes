from odoo import http, _, tools
from odoo.http import request
from odoo.exceptions import UserError


class LoyaltyController(http.Controller):
    @http.route('/api/loyalty-request/<string:cus_id>', type='json', auth='none', methods=["GET"], csrf=False)
    def get_balance(self, cus_id, **params):
        try:
            return {'id': cus_id}
        except Exception as e:
            _logger.error('Error in get_balance: %s', tools.ustr(e))
