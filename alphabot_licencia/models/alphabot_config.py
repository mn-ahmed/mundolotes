# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, Warning


class AccountMove(models.Model):
    _inherit = "account.move"

    fel_alerta_sin_licencia = fields.Char(compute='_compute_fel_alerta_licencia')

    def _compute_fel_alerta_licencia(self):
        self.fel_alerta_sin_licencia = "dummy"



class AlphabotLicense(models.Model):
    _inherit = "res.company"

    alphabot_lic_token = fields.Char(string="Token de licencia de Alphabot")

    alphabot_lic_estado = fields.Char(string="Estado de la licencia Alphabot", compute='Valid_field_ckeck')
    alphabot_lic_fecha = fields.Char(string="Fecha limite de licencia")
    alphabot_lic_activo = fields.Boolean(string="Licencia activa",  default=False)


    def getLicenciaID(self):
        return ""

    def ValidateLicencia(self, Tipo="All"):
        return ""

    def Valid_field_ckeck(self, Tipo="All"):
        self.alphabot_lic_estado = ""
        return ""