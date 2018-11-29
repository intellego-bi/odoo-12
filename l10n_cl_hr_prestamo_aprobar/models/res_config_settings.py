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

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    emp_account = fields.Many2one('account.account', string="Employee Loans Account", readonly=False,
                                  related='account.emp_account',
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Employee Loans Balance Sheet Account (Assets)")

    treasury_account = fields.Many2one('account.account', string="Employee Payment Account", readonly=False,
                                  related='account.treasury_account',
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Employee Loans payment transit Balance Sheet Account (Liability)")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            emp_account=self.env.ref('account.emp_account').id,
            treasury_account=self.env.ref('account.treasury_account').id,
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env.ref('account.emp_account').write({'id': self.emp_account})
        self.env.ref('account.treasury_account').write({'id': self.treasury_account})

