# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import except_orm


class HrLoan(models.Model):
    _name = 'hr.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Loan Request"

    #@api.one
    #@api.onchange('loan_lines')
    @api.multi
    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = loan.loan_amount - total_paid
            self.total_amount = loan.loan_amount
            self.balance_amount = balance_amount
            self.total_paid_amount = total_paid

    @api.multi
    @api.depends('loan_lines', 'loan_lines.amount', 'loan_lines.paid')
    def recompute_loan_amount(self):
        total_paid = 0.0
        calc_balance_amount = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            calc_balance_amount = loan.loan_amount - total_paid
            self.write({'balance_amount': calc_balance_amount})


    name = fields.Char(string="Loan Name", default="/", readonly=True)
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department")
    installment = fields.Integer(string="No Of Installments", default=1)
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today())
    loan_lines = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
    emp_account_id = fields.Many2one('account.account', string="Loan Account", default=lambda self: self.env['account.account'].search([('code', '=', '11050200')], limit=1))
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account", default=lambda self: self.env['account.account'].search([('code', '=', '21050100')], limit=1))
    journal_id = fields.Many2one('account.journal', string="Journal", default=lambda self: self.env['account.journal'].search([('code', '=', 'REMU')], limit=1))
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
    loan_amount = fields.Float(string="Loan Amount", required=True)
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_loan_amount')
    #balance_amount = fields.Float(string="Balance Amount", compute='_compute_loan_amount')
    balance_amount = fields.Float(string="Balance Amount", compute='recompute_loan_amount', store=True, readonly=True)
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_loan_amount')

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
        loan_count = self.env['hr.loan'].search_count([('employee_id', '=', values['employee_id']), ('state', '=', 'approve'),
                                                       ('balance_amount', '!=', 0)])
        if loan_count:
            raise except_orm('Error!', 'The employee has already a pending installment')
        else:
            values['name'] = self.env['ir.sequence'].get('hr.loan.seq') or ' '
            res = super(HrLoan, self).create(values)
            return res

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'refuse'})

    @api.multi
    def action_submit(self):
        self.write({'state': 'waiting_approval_1'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_approve(self):
        for data in self:
            if not data.loan_lines:
                raise except_orm('Error!', 'Please Compute installment')
            else:
                self.write({'state': 'approve'})

    @api.multi
    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for loan in self:
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            amount = loan.loan_amount / loan.installment
            for i in range(1, loan.installment + 1):
                self.env['hr.loan.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            self.balance_amount = loan.loan_amount - total_paid
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
    _name = "hr.loan.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    amount = fields.Float(string="Amount", required=True)
    paid = fields.Boolean(string="Paid")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    move_id = fields.Many2one('account.move', string="Accounting Entry")



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.one
    def _compute_employee_loans(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.loan_count = self.env['hr.loan'].search_count([('employee_id', '=', self.id)])

    loan_count = fields.Integer(string="Loan Count", compute='_compute_employee_loans')


