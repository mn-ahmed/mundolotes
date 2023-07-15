# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, Warning
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    alphabot_estado = fields.Char(string="Estado imp. fiscal", size=1024, copy=False)
    alphabot_cliente_name = fields.Char(string="Cliente imp. fiscal", size=1024)
    alphabot_cliente_ruc = fields.Char(string="RUC imp. fiscal", size=1024)
    alphabot_devol_fact = fields.Char(string="Factura en Devol.", size=1024)

    alphabot_fiscal_data = fields.Boolean(compute='_compute_alphabot_settings', string='Campos para imp. fiscal ...')

  
