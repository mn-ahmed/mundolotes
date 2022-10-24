# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_multi_currency = fields.Boolean(string="Multi Currency")
    apply_exchange_difference = fields.Boolean(string="Apply Exchnage Difference", default=True)
    multi_currency_ids = fields.Many2many("res.currency", string="Seleced Currencies")

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    is_multi_currency_payment = fields.Boolean(string="Multi Currency Payment")
    other_currency_id = fields.Many2one('res.currency', string='Other Currency')
    other_currency_rate = fields.Float(string='Conversion Rate', digits=(12,6),help='Conversion rate from company currency to order currency.')
    other_currency_amount = fields.Float(string='Currency Amount')

class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        result = super(PosOrder, self)._payment_fields(order, ui_paymentline)
        result['other_currency_id'] = ui_paymentline.get('other_currency_id') or False
        result['other_currency_rate'] = ui_paymentline.get('other_currency_rate') or False
        result['other_currency_amount'] = ui_paymentline.get('other_currency_amount') or False
        result['is_multi_currency_payment'] = ui_paymentline.get('is_multi_currency_payment') or False
        return result