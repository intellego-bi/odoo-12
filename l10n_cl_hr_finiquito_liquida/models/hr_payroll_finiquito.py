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
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    hr_settlements_id = fields.Many2one('hr.settlements', string="Final Settlements")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        contract_ids = []

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(str(date_from), "%Y-%m-%d")))
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (
        employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id

        # computation of the salary input
        contracts = self.env['hr.contract'].browse(contract_ids)
        worked_days_line_ids = self.get_worked_day_lines(contracts, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in worked_days_line_ids:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines
        if contracts:
            input_line_ids = self.get_inputs(contracts, date_from, date_to)
            input_lines = self.input_line_ids.browse([])
            for r in input_line_ids:
                input_lines += input_lines.new(r)
            self.input_line_ids = input_lines
        return

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        settle_obj = self.env['hr.settlements'].search([('employee_id', '=', emp_id.id), ('state', '=', 'approve')])
        for settle in settle_obj:
            if date_from <= settle.settle_date <= date_to: # and not settle.paid:
                for result in res:
                    if result.get('code') == 'FIN':
                        result['amount'] = settle.allowance
                        result['hr_settlements_id'] = settle.id
        for settle in settle_obj:
            if date_from <= settle.settle_date <= date_to: # and not settle.paid:
                for result in res:
                    if result.get('code') == 'IAS':
                        result['amount'] = settle.ias_amount
                        result['hr_settlements_id'] = settle.id
        for settle in settle_obj:
            if date_from <= settle.settle_date <= date_to: # and not settle.paid:
                for result in res:
                    if result.get('code') == 'IAP':
                        result['amount'] = settle.iap_amount
                        result['hr_settlements_id'] = settle.id
        for settle in settle_obj:
            if date_from <= settle.settle_date <= date_to: 
                for result in res:
                    if result.get('code') == 'IFP':
                        result['amount'] = settle.ifp_amount
                        result['hr_settlements_id'] = settle.id

        return res

    @api.multi
    def action_payslip_done(self):
        #for line in self.input_line_ids:
        #    if line.loan_line_id:
        #        line.loan_line_id.paid = True
        #        line.loan_line_id.payslip_id = self.id
        #        line.loan_line_id.move_id = self.move_id
        return super(HrPayslip, self).action_payslip_done()
