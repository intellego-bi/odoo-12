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

    #@api.depends('date_maturity')
    #def _default_planned_payment_date(self):
    #    #planned_payment_date = fields.Date.context_today
    #    for lines in self:
    #        c_planned_payment_date = lines.date_maturity
    #                
    #    return c_planned_payment_date


    payment_block = fields.Selection([('payable', 'Payable'), ('blocked', 'Blocked')], string='Payment Block',
      required=True, readonly=False, copy=False, default='payable')
    block_date = fields.Date(string='Block Update Date', readonly=True, copy=False, help='Date of last change in Payment Blocking Reason.')
    planned_payment_date = fields.Date(string='Planned Payment Date', default=_default_planned_payment_date, readonly=False, help='Planned Day for Outgoing payment.')

    @api.onchange('payment_block')
    def onchange_payment_block(self):
        for line in self:
            line.block_date = date.today()

    #@api.multi
    #def compute_planned_payment_date(self):
    #    """ Computes the planned payment date when not manualy set.
    #    """
    #    for line in self:
    #        if not line.planned_payment_date and line.account_id.internal_type == 'payable':
    #            line.planned_payment_date = line.date_maturity
    
    @api.multi
    def write(self, vals):
        if ('account_id' in vals) and self.env['account.account'].browse(vals['account_id']).deprecated:
            raise UserError(_('You cannot use a deprecated account.'))
        if any(key in vals for key in ('account_id', 'journal_id', 'date', 'move_id', 'debit', 'credit')):
            self._update_check()
        if not self._context.get('allow_amount_currency') and any(key in vals for key in ('amount_currency', 'currency_id')):
            #hackish workaround to write the amount_currency when assigning a payment to an invoice through the 'add' button
            #this is needed to compute the correct amount_residual_currency and potentially create an exchange difference entry
            self._update_check()
        #when we set the expected payment date, log a note on the invoice_id related (if any)
        if vals.get('expected_pay_date') and self.invoice_id:
            msg = _('New expected payment date: ') + vals['expected_pay_date'] + '.\n' + vals.get('internal_note', '')
            self.invoice_id.message_post(body=msg) #TODO: check it is an internal note (not a regular email)!

        # INTELLEGO: when we set the maturity date, adjust planned payment date
        if vals.get('date_maturity'):
            for record in self:
                if not record.planned_payment_date:
                    record.planned_payment_date = record.date_maturity

        #when making a reconciliation on an existing liquidity journal item, mark the payment as reconciled
        for record in self:
            if 'statement_line_id' in vals and record.payment_id:
                # In case of an internal transfer, there are 2 liquidity move lines to match with a bank statement
                if all(line.statement_id for line in record.payment_id.move_line_ids.filtered(lambda r: r.id != record.id and r.account_id.internal_type=='liquidity')):
                    record.payment_id.state = 'reconciled'

        result = super(AccountMoveLine, self).write(vals)
        if self._context.get('check_move_validity', True) and any(key in vals for key in ('account_id', 'journal_id', 'date', 'move_id', 'debit', 'credit')):
            move_ids = set()
            for line in self:
                if line.move_id.id not in move_ids:
                    move_ids.add(line.move_id.id)
            self.env['account.move'].browse(list(move_ids))._post_validate()
        return result
