import logging
import json

from odoo import http, _, tools
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class LoyaltyController(http.Controller):
    @http.route('/api/loyalty-request/<string:cus_id>', type='http', auth='none', methods=["GET"], csrf=False)
    def get_balance(self, cus_id, **params):
        try:
            res = {'id': cus_id}
            data = request.env['res.partner'].sudo().search([('phone', '=', cus_id)], limit=1)
            _logger.info(data)
            return http.Response(
                json.dumps(data),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            _logger.error('Error in get_balance: %s', tools.ustr(e))
            return http.Response(
                json.dumps(e),
                status=200,
                mimetype='application/json'
            )