# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    alphabot_pos_category_summary = fields.Boolean(string="Reporte de categorías")
    alphabot_pos_location_summary = fields.Boolean(string="Reporte de ubicación")
    alphabot_pos_order_summary = fields.Boolean(string="Reporte de orden")
    alphabot_pos_payment_summary = fields.Boolean(string="Reporte de pagos")
    alphabot_pos_product_summary = fields.Boolean(string="Reporte de productos")
    alphabot_pos_session_summary = fields.Boolean(string="Reporte de sesión")
