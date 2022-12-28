import logging
import json

from odoo import http, _,exceptions, tools
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class LoyaltyController(http.Controller):
    @http.route('/api/loyalty-request', website='false', type='json', auth='none', methods=["POST"], csrf=False)
    def get_balance(self, **post):
        key = "QM+jWC=4cb6d5!tHShGAKVUJNq1m2^Zv"
        _logger.info(post)
        _logger.info(post.get("vat"))
        try:
            vat = post["vat"]
        except KeyError:
            raise exceptions.AccessDenied(message='`vat` is required.')

        try:
            secret_key = post["secret_key"]
        except KeyError:
            raise exceptions.AccessDenied(message='Invalid Request.')
        try:

            data = request.env['res.partner'].sudo().search([('vat', '=', vat)], limit=1)
            _logger.info("response count: {0}".format(len(data)))

            if len(data) < 1:
                return json.dumps({'success': False,'name': '', 'points': 0, 'message': 'No se encontro'})

            customer = data[0]

            res = {'success': True,'name': customer["name"], 'points': customer["loyalty_points1"], 'message': ''}
            return json.dumps(res)
        except Exception as e:
            _logger.error('Error in get_balance: %s', tools.ustr(e))
            return json.dumps({'success': False,'name': '', 'points': 0, 'message': e["message"]})
