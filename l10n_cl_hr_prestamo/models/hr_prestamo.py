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
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from odoo.exceptions import except_orm
from odoo.exceptions import UserError
from odoo.tools.translate import _

class HrPrestamo(models.Model):
    _name = 'hr.prestamo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Loan Request"

    @api.multi
    def _compute_prestamo_amount(self):
        total_paid = 0.0
        for prestamo in self:
            for line in prestamo.prestamo_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = prestamo.prestamo_amount - total_paid
            self.total_amount = prestamo.prestamo_amount
            self.balance_amount = balance_amount
            self.total_paid_amount = total_paid

    @api.one
    def _compute_pending_amount(self):
        pend_total = 0
        pend_count = 0
        for loan in self: #.prestamo_array:
                for line in loan.prestamo_lines:
                    if not line.paid:
                        pend_total += line.amount
                        pend_count += 1
        self.prestamo_pending_amount = pend_total
        self.prestamo_pending_count = pend_count




    name = fields.Char(string="Loan Name", default="/", readonly=True)
    date = fields.Date(string="Request Date", default=fields.Date.today(), readonly=False)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department")
    installment = fields.Integer(string="No Of Installments", default=1)
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today())
    prestamo_lines = fields.One2many('hr.prestamo.line', 'prestamo_id', string="Loan Line", index=True)
    emp_account_id = fields.Many2one('account.account', string="Employee Loan Account", default=lambda self: self.env['account.account'].search([('code', '=', '11050200')], limit=1))
    treasury_account_id = fields.Many2one('account.account', string="Payments Account", default=lambda self: self.env['account.account'].search([('code', '=', '21050100')], limit=1))
    journal_id = fields.Many2one('account.journal', string="Journal", default=lambda self: self.env['account.journal'].search([('code', '=', 'REMU')], limit=1))
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
    prestamo_amount = fields.Float(string="Loan Amount", required=True)
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_prestamo_amount')
    balance_amount = fields.Float(string="Balance Amount", compute='_compute_prestamo_amount')
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_prestamo_amount')
    move_id = fields.Many2one('account.move', 'Accounting Entry', readonly=True, copy=False)
    prestamo_pending_amount = fields.Float(string="Pending Installments Amount", compute='_compute_pending_amount')
    prestamo_pending_count = fields.Integer(string="N° of Pending Installments", compute='_compute_pending_amount')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    @api.model
    def create(self, values):
        prestamo_count = self.env['hr.prestamo'].search_count([('employee_id', '=', values['employee_id']), ('state', '=', 'approve'),
                                                       ('balance_amount', '!=', 0)])
        prestamo_array = self.env['hr.prestamo'].search([('employee_id', '=', values['employee_id']), ('state', '=', 'approve')])

        pending_total = 0
        pending_count = 0
        for loan in prestamo_array:
                for line in loan.prestamo_lines:
                    if not line.paid:
                        pending_total += line.amount
                        pending_count += 1
        
        pend_total = str('{0:,.0f}'.format(pending_total)).replace(",", ".")
        pend_count = str(pending_count)

        if pending_total > 0:
            raise UserError(_(
                              'Error! This employee has %s pending installment(s) for a total of %s %s') % (
                              pend_count, self.env.user.company_id.currency_id.name, pend_total))
        else:
            values['name'] = self.env['ir.sequence'].get('hr.prestamo.seq') or ' '
            res = super(HrPrestamo, self).create(values)
            return res

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'refuse'})

    @api.multi
    def action_submit(self):
        for prestamo in self:
            for line in prestamo.prestamo_lines:
                if line.amount <= 0:
                    raise UserError(_(
                              'Error: Enter positive installment amounts'))

        # Read Loan Accounting Settings from res.config.settings
        ICPSudo = self.env['ir.config_parameter'].sudo()

        config_read = int(ICPSudo.get_param('account.hr_emp_account_id'))
        if config_read:
            self.emp_account_id = config_read

        config_read = int(ICPSudo.get_param('account.hr_treasury_account_id'))
        if config_read:
            self.treasury_account_id = config_read
        
        config_read = int(ICPSudo.get_param('account.hr_journal_id'))
        if config_read:
            config_ok = 0
            self.journal_id = config_read

        if self.journal_id:
            self.write({'state': 'waiting_approval_1'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_approve(self):
        for data in self:
            if not data.prestamo_lines:
                raise UserError(_(
                              'Error! Please Compute installment'))
            else:
                self.write({'state': 'approve'})

    @api.multi
    def compute_installment(self):
        """This automatically creates payment installment plan for the Loan
        based on the payment start date and the number of installments.
        """
        total_lines = 0
        
        for prestamo in self:
            date_pay = datetime.strptime(str(prestamo.payment_date), '%Y-%m-%d')
            for line in prestamo.prestamo_lines:
                total_lines += line.amount
                date_last = datetime.strptime(str(line.date), '%Y-%m-%d')
            if int(total_lines) > 0:
               date_pay = date_last 
            if int(total_lines) >= int(prestamo.prestamo_amount):
                raise UserError(_('Warning! Installments already computed'))
            else:
                amount = (prestamo.prestamo_amount - total_lines) / prestamo.installment
                date_start = date_pay
                for i in range(1, prestamo.installment + 1):
                    self.env['hr.prestamo.line'].create({
                        'date': date_start,
                        'amount': amount,
                        'currency_id': prestamo.currency_id.id,
                        'employee_id': prestamo.employee_id.id,
                        'prestamo_id': prestamo.id})
                    date_start = date_pay + relativedelta(months=i)
        return True


class InstallmentLine(models.Model):
    _name = "hr.prestamo.line"
    _description = "Installment Line"

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    date = fields.Date(string="Payment Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    amount = fields.Float(string="Amount", required=True)
    paid = fields.Boolean(string="Paid")
    prestamo_id = fields.Many2one('hr.prestamo', string="Loan Ref.")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    move_id = fields.Many2one('account.move', related="payslip_id.move_id", string="Accounting Entry")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.one
    def _compute_employee_prestamo(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.prestamo_count = self.env['hr.prestamo'].search_count([('employee_id', '=', self.id)])
        
        self.prestamo_array = self.env['hr.prestamo'].search([('employee_id', '=', self.id), ('state', '=', 'approve')])
        pend_total = 0
        pend_count = 0
        for loan in self.prestamo_array:
                for line in loan.prestamo_lines:
                    if not line.paid:
                        pend_total += line.amount
                        pend_count += 1
        self.emp_pending_amount = pend_total
        self.emp_pending_count = pend_count

    prestamo_count = fields.Integer(string="Loan Count", compute='_compute_employee_prestamo')
    emp_pending_amount = fields.Integer(string="Pending Installments Amount", compute='_compute_employee_prestamo')
    emp_pending_count = fields.Integer(string="Number of Pending Installments", compute='_compute_employee_prestamo')

