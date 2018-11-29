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

class AccConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    prestamo_approve = fields.Boolean(default=False, string="Approval from Accounting Department",
                                  help="Loan Approval from account manager")

    emp_account_id = fields.Many2one('account.account', string="Employee Loans Account", readonly=False,
                                  #related='account.emp_account',
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Employee Loans Balance Sheet Account (Assets)")

    treasury_account_id = fields.Many2one('account.account', string="Employee Payment Account", readonly=False,
                                  #related='account.treasury_account',
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Employee Loans payment transit Balance Sheet Account (Liability)")

    @api.model
    def get_values(self):
        res = super(AccConfig, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            prestamo_approve=ICPSudo.get_param('account.prestamo_approve'),
            emp_account_id=int(ICPSudo.get_param('account.emp_account_id')),
            treasury_account_id=int(ICPSudo.get_param('account.treasury_account_id')),
        )
        return res

    @api.multi
    def set_values(self):
        super(AccConfig, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('account.prestamo_approve', self.prestamo_approve)
        ICPSudo.set_param('account.emp_account_id', self.emp_account_id.id)
        ICPSudo.set_param('account.treasury_account_id', self.treasury_account_id.id)



