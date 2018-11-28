# -*- coding: utf-8 -*-
#import datetime
from datetime import datetime
from odoo import fields, models, api, exceptions, _
from odoo.exceptions import ValidationError,UserError
date_format = "%Y-%m-%d"


class FinalSettlements(models.Model):
    _name = 'hr.settlements'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HR Settlement"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validated'),
        ('approve', 'Approved'),
        ('cancel', 'Cancelled'),
    ], default='draft', track_visibility='onchange')

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department")
    joined_date = fields.Date(string="Joined Date")
    settle_date = fields.Date(string="Settlement Date")
    worked_years = fields.Integer(string="Total Work Years")
    worked_months = fields.Integer(string="Total Work Months")
    worked_days = fields.Integer(string="Total Work Days")
    last_month_salary = fields.Integer(string="Last Salary", required=True, default=0)
    last_2_month_salary = fields.Integer(string="2nd Last Salary ", required=False, default=0)
    last_3_month_salary = fields.Integer(string="3rd Last Salary ", required=False, default=0)
    average_salary = fields.Integer(string="Average Salary (past 3 months)", required=True, default=0)
    valor_uf = fields.Float(string="Valor UF", required="True")
    allowance = fields.Char(string="Dearness Allowance", default=0)
    gratuity_amount = fields.Integer(string="Gratuity Payable", required=True, default=0, readony=True, help=("Gratuity is calculated based on 							the equation Last salary * Number of years of service"))

    reason = fields.Selection([('renuncia', 'Renuncia Voluntaria'),
                               ('despido', 'Despido')], string="Settlement Reason", required="True")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    # assigning the sequence for the record
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.settlement')
        return super(FinalSettlements, self).create(vals)

    # Check whether any Settlement request already exists
    @api.onchange('employee_id')
    @api.depends('employee_id')
    def check_request_existence(self):
        for rec in self:
            if rec.employee_id:
                settlement_request = self.env['hr.settlements'].search([('employee_id', '=', rec.employee_id.id),
                                                                           ('state', 'in', ['draft', 'validate', 'approve'])])
                if settlement_request:

                    raise ValidationError(_('A Settlement request is already processed'
                                                ' for this employee'))

    @api.multi
    def validate_function(self):
        # calculating the years of work by the employee
   
        #end_date = datetime.strptime(str(datetime.now().year) + "-" + str(datetime.now().month) + "-" +str(datetime.now().day), date_format)
        end_date = datetime.strptime(str(self.settle_date.year) + "-" + str(self.settle_date.month) + "-" +str(self.settle_date.day), date_format)
        start_date = datetime.strptime(str(self.joined_date.year) + "-" + str(self.joined_date.month) + "-" +str(self.joined_date.day), date_format)
        worked_days = (end_date - start_date).days - 1
        worked_years = int(round(worked_days / 365))
        worked_months = int(round(worked_days / 365 * 12))
        if worked_years >= 0.5:

            self.worked_years = worked_years
            self.worked_months = worked_months
            self.worked_days = worked_days

            cr = self._cr  # find out the correct  date of last salary of  employee
            #query = """select amount from hr_payslip_line psl 
            #           inner join hr_payslip ps on ps.id=psl.slip_id
            #           where ps.employee_id="""+str(self.employee_name.id)+\
            #           """and ps.state='done' and psl.code='NET' 
            #           order by ps.date_from desc limit 1"""

            query = """select amount from hr_payslip_line psl 
                       inner join hr_payslip ps on ps.id=psl.slip_id
                       where ps.employee_id="""+str(self.employee_id.id)+\
                       """and ps.state='done' and psl.code='HAB' 
                       order by ps.date_from desc limit 3"""

            cr.execute(query)
            data = cr.fetchall()
            if data:
                 last_salary = data[0][0]
                 last_2_salary = data[1][0]
                 last_3_salary = data[2][0]
            else:
                last_salary = 0
                last_2_salary = 0
                last_3_salary = 0

            ls_a = 1
            if last_2_salary > 0:
               ls_b = 1
            if last_3_salary > 0:
               ls_c = 1   

            self.average_salary = ( last_salary + last_2_salary + last_3_salary ) / ( ls_a + ls_b + ls_c )
            self.last_month_salary = last_salary
            self.last_2_month_salary = last_2_salary
            self.last_3_month_salary = last_3_salary

            cr = self._cr  # find out the correct  date of last salary of  employee

            query = """select uf from hr_indicadores hri  
                       inner join hr_payslip ps on ps.indicadores_id=hri.id
                       where ps.employee_id="""+str(self.employee_id.id)+\
                       """and ps.state='done' 
                       order by ps.date_from desc limit 1"""

            cr.execute(query)
            data = cr.fetchall()
            if data:
                 valor_uf = data[0][0]
            else:
                valor_uf = 0

            self.valor_uf = valor_uf

            self.write({
                'state': 'validate'})
        else:

            self.write({
                'state': 'draft'})
            self.worked_years = worked_years

            raise exceptions.except_orm(_('Employee Working Period is less than 1 Year'),
                                  _('Only an Employee with minimum 1 years of working, will get the Settlement advantage'))

    def approve_function(self):

        if not self.allowance.isdigit() :
            raise ValidationError(_('Allowance value should be numeric !!'))

        self.write({
            'state': 'approve'
        })

        tope = self.valor_uf * 90
        if self.average_salary > tope:
            amount = ((tope + int(self.allowance)) * int(self.worked_years))
        else:
            amount = ((self.average_salary + int(self.allowance)) * int(self.worked_years) * 1) / 1
        self.gratuity_amount = round(amount) if self.state == 'approve' else 0

    def cancel_function(self):
        self.write({
            'state': 'cancel'
        })

    def draft_function(self):
        self.write({
            'state': 'draft'
        })
        self.worked_years = 0
        self.worked_months = 0
        self.worked_days = 0

