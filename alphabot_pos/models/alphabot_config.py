# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    alphabot_cliente_id = fields.Many2one('res.partner', string="Seleccionar cliente")


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_amount(self):
        for rec in self:
            super(AccountMove, rec)._compute_amount()
            pos_invoices = rec.filtered(lambda i: i.move_type in ['out_invoice', 'out_refund'] and i.pos_order_ids)
            _logger.debug("_compute_amount")

            for invoice in pos_invoices:

                pos_order = rec.env['pos.order'].search([('account_move', '=', invoice.id)])
                pos_order_payments = rec.env['pos.payment'].search([('pos_order_id', '=', pos_order.id)])
                split_payment = 0
                for payment in pos_order_payments:
                    if payment.payment_method_id.split_transactions:
                        split_payment += 1
                if split_payment == 0:
                    invoice.payment_state = 'paid'


