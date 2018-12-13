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
from odoo import models, api
from odoo.exceptions import except_orm


class HrPrestamoAcc(models.Model):
    _inherit = 'hr.prestamo'

    @api.multi
    def action_approve(self):
        """This create account move for request.
            """
        prestamo_approve = self.env['ir.config_parameter'].sudo().get_param('account.prestamo_approve')
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise except_orm('Warning', 'You must Define a contract for employee')
        if not self.prestamo_lines:
            raise except_orm('Warning', 'You must compute installment before Approval')
        if prestamo_approve:
            self.write({'state': 'waiting_approval_2'})
        else:
            if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
                raise except_orm('Warning',
                                 "You must enter employee account & Treasury account and journal to approve ")
            if not self.prestamo_lines:
                raise except_orm('Warning', 'You must compute Loan Request before Approved')
            timenow = time.strftime('%Y-%m-%d')
            for prestamo in self:
                if prestamo.currency_id.name == 'CLP':
                    amount = prestamo.prestamo_amount
                else:
                    amount = prestamo.currency_id._convert(prestamo.prestamo_amount, self.env.user.company_id.currency_id, prestamo.company_id, prestamo.date)
                    currency_id = prestamo.currency_id
                    amount_currency = prestamo.prestamo_amount
                prestamo_name = prestamo.employee_id.name
                reference = prestamo.name
                journal_id = prestamo.journal_id.id
                date = prestamo.date
                # debit_account_id = loan.treasury_account_id.id
                # credit_account_id = loan.emp_account_id.id
                credit_account_id = prestamo.treasury_account_id.id
                debit_account_id = prestamo.emp_account_id.id
                debit_vals = {
                    'name': prestamo_name,
                    # Insert Intellego-BI: Empleado como Partner en contabilizaciones
                    'partner_id' : prestamo.employee_id.address_home_id.id,
                    'account_id': debit_account_id,
                    'journal_id': journal_id,
                    'date': date, #timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'currency_id': prestamo.currency_id.id,
                    'amount_currency': prestamo.prestamo_amount,
                    'prestamo_id': prestamo.id,
                }
                credit_vals = {
                    'name': prestamo_name,
                    # Insert Intellego-BI: Empleado como Partner en contabilizaciones
                    'partner_id' : prestamo.employee_id.address_home_id.id,
                    'account_id': credit_account_id,
                    'journal_id': journal_id,
                    'date': date, #timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'currency_id': prestamo.currency_id.id,
                    'amount_currency': -prestamo.prestamo_amount,
                    'prestamo_id': prestamo.id,
                }
                vals = {
                    'name': 'Préstamo a' + ' ' + prestamo_name,
                    'narration': prestamo_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'date': date, #timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                prestamo.write({'move_id': move.id})
                move.post()
            self.write({'state': 'approve'})
        return True

    @api.multi
    def action_double_approve(self):
        """This create account move for request in case of double approval.
            """
        if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
            raise except_orm('Warning', "You must enter employee account & Treasury account and journal to approve ")
        if not self.prestamo_lines:
            raise except_orm('Warning', 'You must compute Loan Request before Approved')
        timenow = time.strftime('%Y-%m-%d')
        for prestamo in self:
            if prestamo.currency_id.name == 'CLP':
                amount = prestamo.prestamo_amount
            else:
                amount = prestamo.currency_id._convert(prestamo.prestamo_amount, self.env.user.company_id.currency_id, prestamo.company_id, prestamo.date)
                currency_id = prestamo.currency_id
                amount_currency = prestamo.prestamo_amount

            #amount = prestamo.prestamo_amount
            prestamo_name = prestamo.employee_id.name
            reference = prestamo.name
            journal_id = prestamo.journal_id.id
            date = prestamo.date
            # debit_account_id = loan.treasury_account_id.id
            # credit_account_id = loan.emp_account_id.id
            credit_account_id = prestamo.treasury_account_id.id
            debit_account_id = prestamo.emp_account_id.id
            debit_vals = {
                'name': prestamo_name,
                'account_id': debit_account_id,
                # Insert Intellego-BI: Empleado como Partner en contabilizaciones
                'partner_id' : prestamo.employee_id.address_home_id.id,
                'journal_id': journal_id,
                'date': date, #timenow,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
                'currency_id': prestamo.currency_id.id,
                'amount_currency': prestamo.prestamo_amount,
                'prestamo_id': prestamo.id,
            }
            credit_vals = {
                'name': prestamo_name,
                'account_id': credit_account_id,
                # Insert Intellego-BI: Empleado como Partner en contabilizaciones
                'partner_id' : prestamo.employee_id.address_home_id.id,
                'journal_id': journal_id,
                'date': date, #timenow,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
                'currency_id': prestamo.currency_id.id,
                'amount_currency': -prestamo.prestamo_amount,
                'prestamo_id': prestamo.id,
            }
            vals = {
                'name': 'Préstamo a' + ' ' + prestamo_name,
                'narration': prestamo_name,
                'ref': reference,
                'journal_id': journal_id,
                'date': date, #timenow,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            prestamo.write({'move_id': move.id})
            move.post()
        self.write({'state': 'approve'})
        return True


class HrPrestamoLineAcc(models.Model):
    _inherit = "hr.prestamo.line"

    @api.one
    def action_paid_amount(self):
        """This create the account move line for payment of each installment.
            """
        #timenow = time.strftime('%Y-%m-%d')
        #for line in self:
        #    if line.prestamo_id.state != 'approve':
        #        raise except_orm('Warning', "Loan Request must be approved")
        #    amount = line.amount
        #    prestamo_name = line.employee_id.name
        #    reference = line.prestamo_id.name
        #    journal_id = line.prestamo_id.journal_id.id
            # debit_account_id = line.loan_id.emp_account_id.id
            # credit_account_id = line.loan_id.treasury_account_id.id
        #    credit_account_id = line.prestamo_id.emp_account_id.id
        #    debit_account_id = line.prestamo_id.treasury_account_id.id
        #    debit_vals = {
        #        'name': prestamo_name,
        #        'account_id': debit_account_id,
        #        # Insert Intellego-BI: Empleado como Partner en contabilizaciones
        #        'partner_id' : line.employee_id.address_home_id.id,
        #        'journal_id': journal_id,
        #        'date': timenow,
        #        'debit': amount > 0.0 and amount or 0.0,
        #        'credit': amount < 0.0 and -amount or 0.0,
        #    }
        #    credit_vals = {
        #        'name': prestamo_name,
        #        'account_id': credit_account_id,
        #        # Insert Intellego-BI: Empleado como Partner en contabilizaciones
        #        'partner_id' : line.employee_id.address_home_id.id,
        #        'journal_id': journal_id,
        #        'date': timenow,
        #        'debit': amount < 0.0 and -amount or 0.0,
        #        'credit': amount > 0.0 and amount or 0.0,
        #    }
        #    vals = {
        #        'name': 'Préstamo a' + ' ' + prestamo_name,
        #        'narration': prestamo_name,
        #        'ref': reference,
        #        'journal_id': journal_id,
        #        'date': timenow,
        #        'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
        #    }
        #    move = self.env['account.move'].create(vals)
        #    line.write({'move_id': move.id})
        #    move.post()
        return True


class HrPayslipAcc(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        for line in self.input_line_ids:
            if line.prestamo_line_id:
                line.prestamo_line_id.action_paid_amount()
        return super(HrPayslipAcc, self).action_payslip_done()
