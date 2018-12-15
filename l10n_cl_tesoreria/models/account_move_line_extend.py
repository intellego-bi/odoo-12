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
from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
import odoo.addons.decimal_precision as dp



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _description = "Journal Item"

    def _default_planned_payment_date(self):
        planned_payment_date = fields.Date.context_today    
        return planned_payment_date

    payment_block = fields.Selection([('payable', 'Payable'), ('blocked', 'Blocked')], string='Payment Block',
      required=True, readonly=False, copy=False, default='payable')
    block_date = fields.Date(string='Block Update Date', readonly=True, copy=False, help='Date of last change in Payment Blocking Reason.')
    planned_payment_date = fields.Date(string='Planned Payment Date', default=_default_planned_payment_date, readonly=False, help='Planned Day for Outgoing payment.')

    @api.onchange('payment_block')
    def onchange_payment_block(self):
        for line in self:
            line.block_date = date.today()

    @api.multi
    def _compute_planned_payment_date(self):
        """ Computes the planned payment date when not manualy set.
        """
        for line in self:
            if not line.planned_payment_date and line.account_id.internal_type == 'payable':
                line.planned_payment_date = line.date_maturity
    
