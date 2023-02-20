import logging
import json

from odoo import http, _,exceptions, tools
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class OdooCustomReportController(http.Controller):
    @http.route('/api/loyalty-request', website='false', type='json', auth='none', methods=["POST"], csrf=False)
    def get_orders(self, **post):
        _logger.info(post)
        try:

            data = request.env['report.pos.order'].sudo().search([])
            _logger.info("response count: {0}".format(len(data)))

            if len(data) < 1:
                return json.dumps({'success': True, 'data': null })



            res = {'success': True, 'data': data}
            return json.dumps(res)
        except Exception as e:
            _logger.error('Error in get_orders: %s', tools.ustr(e))
            return json.dumps({'success': False, 'data': null})
