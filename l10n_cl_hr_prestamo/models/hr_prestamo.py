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
from odoo.exceptions import except_orm


class HrPrestamo(models.Model):
    _name = 'hr.prestamo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Loan Request"

    #@api.one
    #@api.onchange('prestamo_lines')
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

    @api.multi
    @api.depends('prestamo_lines', 'prestamo_lines.amount', 'prestamo_lines.paid')
    def recompute_prestamo_amount(self):
        total_paid = 0.0
        calc_balance_amount = 0.0
        for prestamo in self:
            for line in prestamo.prestamo_lines:
                if line.paid:
                    total_paid += line.amount
            calc_balance_amount = prestamo.prestamo_amount - total_paid
            self.write({'balance_amount': calc_balance_amount})


    name = fields.Char(string="Loan Name", default="/", readonly=True)
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department")
    installment = fields.Integer(string="No Of Installments", default=1)
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today())
    prestamo_lines = fields.One2many('hr.prestamo.line', 'prestamo_id', string="Loan Line", index=True)
    emp_account_id = fields.Many2one('account.account', string="Loan Account", default=lambda self: self.env['account.account'].search([('code', '=', '11050200')], limit=1))
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account", default=lambda self: self.env['account.account'].search([('code', '=', '21050100')], limit=1))
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
    #balance_amount = fields.Float(string="Balance Amount", compute='recompute_loan_amount', store=True) #, readonly=True)
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_prestamo_amount')

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
        if prestamo_count:
            raise except_orm('Error!', 'The employee has already a pending installment')
        else:
            values['name'] = self.env['ir.sequence'].get('hr.prestamo.seq') or ' '
            res = super(HrPrestamo, self).create(values)
            return res

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'refuse'})

    #('key', '=', 'account.hr_emp_account_id')
    @api.multi
    def action_submit(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        hr_emp_acct = ICPSudo.get_param('account.hr_emp_account_id')
        #hr_emp_acct = self.env['res.config.settings'].search([], order='id desc')
        raise except_orm('Info:', 'Account %s' % (hr_emp_acct[1]))
        self.write({'state': 'waiting_approval_1'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_approve(self):
        for data in self:
            if not data.prestamo_lines:
                raise except_orm('Error!', 'Please Compute installment')
            else:
                self.write({'state': 'approve'})

    @api.multi
    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for prestamo in self:
            date_start = datetime.strptime(str(prestamo.payment_date), '%Y-%m-%d')
            amount = prestamo.prestamo_amount / prestamo.installment
            for i in range(1, prestamo.installment + 1):
                self.env['hr.prestamo.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': prestamo.employee_id.id,
                    'prestamo_id': prestamo.id})
                date_start = date_start + relativedelta(months=1)
        total_paid = 0.0
        for prestamo in self:
            for line in prestamo.prestamo_lines:
                if line.paid:
                    total_paid += line.amount
            self.balance_amount = prestamo.prestamo_amount - total_paid
        return True


    #@api.onchange('paid')
    #@api.multi
    #def recompute_loan_balance(self):
    #    total_paid = 0.0
    #    loan_amount = 0.0
    #    for loan in self:
    #        for line in loan.loan_lines:
    #            if line.paid:
    #                total_paid += line.amount
    #        self.balance_amount = loan.loan_amount - total_paid




class InstallmentLine(models.Model):
    _name = "hr.prestamo.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    amount = fields.Float(string="Amount", required=True)
    paid = fields.Boolean(string="Paid")
    prestamo_id = fields.Many2one('hr.prestamo', string="Loan Ref.")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    move_id = fields.Many2one('account.move', string="Accounting Entry")



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.one
    def _compute_employee_prestamo(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.prestamo_count = self.env['hr.prestamo'].search_count([('employee_id', '=', self.id)])

    prestamo_count = fields.Integer(string="Loan Count", compute='_compute_employee_prestamo')


