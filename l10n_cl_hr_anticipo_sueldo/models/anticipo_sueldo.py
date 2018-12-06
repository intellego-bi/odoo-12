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
import time
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import except_orm
from odoo import exceptions

class AnticipoSueldoPago(models.Model):
    _name = "anticipo.sueldo"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', readonly=True, default=lambda self: 'Nueva Solicitud/')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.today())
    reason = fields.Text(string='Reason')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    advance = fields.Float(string='Advance', required=True)
    payment_method = fields.Many2one('account.journal', string='Payment Method')
    exceed_condition = fields.Boolean(string='Exceed Maximum %',
                                      help="The Advance is greater than the maximum percentage in salary structure")
    
    department = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                  string="Department")
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submitted'),
                              ('waiting_approval', 'Waiting Approval'),
                              ('approve', 'Approved'),
                              ('cancel', 'Cancelled'),
                              ('reject', 'Rejected')], string='Status', default='draft', track_visibility='onchange')
    debit = fields.Many2one('account.account', string='Debit Account')
    credit = fields.Many2one('account.account', string='Credit Account')
    journal = fields.Many2one('account.journal', string='Journal', default=lambda self: self.env['account.journal'].search([('type', '=', 'general')], limit=1))
    employee_contract_id = fields.Many2one('hr.contract', string='Contract')
    move_id = fields.Many2one('account.move', 'Accounting Entry', readonly=True, copy=False)
    

    @api.onchange('employee_id')
    def onchange_employee_id(self):
       # Read Accounting Settings from res.config.settings
        ICPSudo = self.env['ir.config_parameter'].sudo()
        config_read = int(ICPSudo.get_param('account.hr_debit_account_id'))
        if config_read:
            self.debit = config_read
        config_read = int(ICPSudo.get_param('account.hr_credit_account_id'))
        if config_read:
            self.credit = config_read
        config_read = int(ICPSudo.get_param('account.hr_anticipo_journal_id'))
        if config_read:
            self.journal = config_read

        department_id = self.employee_id.department_id.id
        domain = [('employee_id', '=', self.employee_id.id)]
        return {'value': {'department': department_id}, 'domain': {
            'employee_contract_id': domain,
        }}

    @api.onchange('company_id')
    def onchange_company_id(self):
        company = self.company_id
        domain = [('company_id.id', '=', company.id)]
        result = {
            'domain': {
                'journal': domain,
            },

        }
        return result

    @api.one
    def submit_to_manager(self):
        # Read Accounting Settings from res.config.settings
        ICPSudo = self.env['ir.config_parameter'].sudo()
        config_read = int(ICPSudo.get_param('account.hr_debit_account_id'))
        if config_read:
            self.debit = config_read
        config_read = int(ICPSudo.get_param('account.hr_credit_account_id'))
        if config_read:
            self.credit = config_read
        config_read = int(ICPSudo.get_param('account.hr_anticipo_journal_id'))
        if config_read:
            self.journal = config_read

        self.state = 'submit'

    @api.one
    def cancel(self):
        self.state = 'cancel'

    @api.one
    def reject(self):
        self.state = 'reject'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('hr.anticipo.seq') or ' '
        res_id = super(AnticipoSueldoPago, self).create(vals)
        return res_id

    @api.one
    def approve_request(self):
        """This Approve the employee salary advance request.
                   """
        # Read Accounting Settings from res.config.settings
        ICPSudo = self.env['ir.config_parameter'].sudo()
        config_read = int(ICPSudo.get_param('account.hr_debit_account_id'))
        if config_read:
            self.debit = config_read
        config_read = int(ICPSudo.get_param('account.hr_credit_account_id'))
        if config_read:
            self.credit = config_read
        config_read = int(ICPSudo.get_param('account.hr_anticipo_journal_id'))
        if config_read:
            self.journal = config_read

        emp_obj = self.env['hr.employee']
        address = emp_obj.browse([self.employee_id.id]).address_home_id
        if not address.id:
            raise except_orm('Error!', 'Define home address for employee')
        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise except_orm('Error!', 'Advance can be requested once in a month')
        if not self.employee_contract_id:
            raise except_orm('Error!', 'Define a contract for the employee')
        struct_id = self.employee_contract_id.struct_id
        #if not struct_id.max_percent or not struct_id.advance_date:
        #    raise except_orm('Error!', 'Max percentage or advance days are not provided in Contract')
        adv = self.advance
        #amt = (self.employee_contract_id.struct_id.max_percent * self.employee_contract_id.wage) / 100
        #if adv > amt and not self.exceed_condition:
        #    raise except_orm('Error!', 'Advance amount is greater than allotted')

        if not self.advance:
            raise except_orm('Warning', 'You must Enter the Salary Advance amount')
        payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id),
                                                     ('state', '=', 'done'), ('date_from', '<=', self.date),
                                                     ('date_to', '>=', self.date)])
        if payslip_obj:
            raise except_orm('Warning', "This month salary already calculated")

        for slip in self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id)]):
            slip_moth = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().month
            if current_month == slip_moth + 1:
                slip_day = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().day
                current_day = datetime.strptime(str(self.date), '%Y-%m-%d').date().day
                if current_day - slip_day < struct_id.advance_date:
                    raise exceptions.Warning(
                        _('Request can be done after "%s" Days From prevoius month salary') % struct_id.advance_date)
        hr_anticipo_approve = self.env['ir.config_parameter'].sudo().get_param('account.hr_anticipo_approve')
        self.state = 'waiting_approval'

    @api.one
    def approve_request_acc_dept(self):
        """This Approve the employee salary advance request from accounting department.
                   """
        # Read Accounting Settings from res.config.settings
        ICPSudo = self.env['ir.config_parameter'].sudo()
        config_read = int(ICPSudo.get_param('account.hr_debit_account_id'))
        if config_read:
            self.debit = config_read
        config_read = int(ICPSudo.get_param('account.hr_credit_account_id'))
        if config_read:
            self.credit = config_read
        config_read = int(ICPSudo.get_param('account.hr_anticipo_journal_id'))
        if config_read:
            self.journal = config_read

        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise except_orm('Error!', 'Advance can be requested once in a month')
        if not self.debit or not self.credit or not self.journal:
            raise except_orm('Warning', "You must enter Debit & Credit account and journal to approve ")
        if not self.advance:
            raise except_orm('Warning', 'You must Enter the Salary Advance amount')

        move_obj = self.env['account.move']
        timenow = time.strftime('%Y-%m-%d')
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0

        for request in self:
            amount = request.advance
            request_name = request.employee_id.name
            reference = request.name
            journal_id = request.journal.id
            debit_account_id = request.debit.id
            credit_account_id = request.credit.id

            debit_vals = {
                'name': request_name,
                'partner_id' : request.employee_id.address_home_id.id,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                #'date': timenow,
                'date': date,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
                'currency_id': self.currency_id.id,
                #'prestamo_id': prestamo.id,
                }
            credit_vals = {
                'name': request_name,
                'partner_id' : request.employee_id.address_home_id.id,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                #'date': timenow,
                'date': date,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
                'currency_id': self.currency_id.id,
                #'prestamo_id': prestamo.id,
                }
            vals = {
                'name': 'Salary Advance for ' + request_name,
                'narration': request_name,
                'ref': reference,
                'journal_id': journal_id,
                #'date': timenow,
                'date': date,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
            move = self.env['account.move'].create(vals)
            request.write({'move_id': move.id})
            move.post()
            self.write({'state': 'approve'})
            return True
