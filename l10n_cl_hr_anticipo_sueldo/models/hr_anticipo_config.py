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

class HRAnticipoConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    hr_anticipo_approve = fields.Boolean(default=False, string="HR Salary Advance Approval from Accounting Department",
                                  help="Salary Advance Approval from account manager")

    hr_debit_account_id = fields.Many2one('account.account', string="HR Salary Advance Debit Account", readonly=False,
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Salary Advance Balance Sheet Account (Assets)")

    hr_credit_account_id = fields.Many2one('account.account', string="HR Salary Advance Credit Account", readonly=False,
                                  domain=lambda self: [('reconcile', '=', True)],
                                  help="Salary Advance payment transit Balance Sheet Account (Liability)")

    hr_anticipo_journal_id = fields.Many2one('account.journal', string="HR Salary Advance Journal", 
                                  domain=lambda self: [('code', '=', 'REMU')],
                                  help="Accounting Journal used for Salary Advance to Employee")

    @api.model
    def get_values(self):
        res = super(HRAnticipoConfig, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            hr_anticipo_approve=ICPSudo.get_param('account.hr_anticipo_approve'),
            hr_debit_account_id=int(ICPSudo.get_param('account.hr_debit_account_id')),
            hr_credit_account_id=int(ICPSudo.get_param('account.hr_credit_account_id')),
            hr_anticipo_journal_id=int(ICPSudo.get_param('account.hr_anticipo_journal_id')),
        )
        return res

    @api.multi
    def set_values(self):
        super(HRAnticipoConfig, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('account.hr_anticipo_approve', self.hr_anticipo_approve)
        ICPSudo.set_param('account.hr_debit_account_id', self.hr_debit_account_id.id)
        ICPSudo.set_param('account.hr_credit_account_id', self.hr_credit_account_id.id)
        ICPSudo.set_param('account.hr_anticipo_journal_id', self.hr_anticipo_journal_id.id)



