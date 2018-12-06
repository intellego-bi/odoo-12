# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2017-TODAY Intellego Business Intelligence S.A.(<http://www.intellego-bi.com>).
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
###################################################################################
from odoo import models, fields, api, _

class AccCurrConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    cl_update_active = fields.Boolean(default=True, string="Chile Update Currency Rates from SBIF",
                                  help="Enabla automatic rate download from SBIF Chile")

    cl_sbif_api_key  = fields.Char(string='SBIF API Key', 
                                   default='e96f651e08214ed0060771f21d11cdeb3b8b3305', 
                                   required=True,
                                   help="You must get your private API Key from https://api.sbif.cl "
                                        "in order to use this service.")

    @api.model
    def get_values(self):
        res = super(AccCurrConfig, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            cl_update_active=ICPSudo.get_param('account.cl_update_active'),
            cl_sbif_api_key=ICPSudo.get_param('account.cl_sbif_api_key'),
        )
        return res

    @api.multi
    def set_values(self):
        super(AccCurrConfig, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('account.cl_update_active', self.cl_update_active)
        ICPSudo.set_param('account.cl_sbif_api_key', self.cl_sbif_api_key)




