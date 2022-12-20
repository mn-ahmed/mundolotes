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

            data = request.env['res.partner'].sudo().search([('phone', '=', cus_id)], limit=1)
            _logger.info("response count: {0}".format(len(data)))
            customer = data[0]
            all_fields = customer.fields_get_keys()
            for field in all_fields:
                _logger.info(field)
            res = {'id': cus_id, 'name': customer["name"]}
            return http.Response(
                json.dumps(res),
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
