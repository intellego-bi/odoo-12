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
import datetime
from odoo import fields, models, api, exceptions, _
from odoo.exceptions import ValidationError,UserError
date_format = "%Y-%m-%d"


class EmployeeGratuity(models.Model):
    _name = 'hr.gratuity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Employee Gratuity"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validated'),
        ('approve', 'Approved'),
        ('cancel', 'Cancelled')],
        default='draft', track_visibility='onchange')
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    employee_name = fields.Many2one('hr.resignation', string='Employee', required=True,
                                    domain="[('state', '=', 'approved')]")
    joined_date = fields.Date(string="Joined Date", readonly=True)
    worked_years = fields.Integer(string="Total Work Years", readonly=True)
    last_month_salary = fields.Integer(string="Last Salary", required=True, default=0)
    allowance = fields.Char(string="Dearness Allowance", default=0)
    gratuity_amount = fields.Integer(string="Gratuity Payable", required=True, default=0,
                                  readony=True, help=("Gratuity is calculated based on the "
                                  "equation Last salary * Number of years of service * 15 / 26 "))
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', 'Company',  default=lambda self: self.env.user.company_id)

    # assigning the sequence for the record
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.gratuity')
        return super(EmployeeGratuity, self).create(vals)

    # Check whether any Gratuity request already exists
    @api.onchange('employee_name')
    @api.depends('employee_name')
    def check_request_existence(self):
        for rec in self:
            if rec.employee_name:

                gratuity_request = self.env['hr.gratuity'].search([('employee_name', '=', rec.employee_name.id),
                                                                   ('state', 'in', ['draft', 'validate', 'approve', 'cancel'])])
                if gratuity_request:
                    raise ValidationError(_('A Settlement request is already processed'
                                            ' for this employee'))

    @api.multi
    def validate_function(self):
        # calculating the years of work by the employee
        worked_years = int(datetime.datetime.now().year) - int(str(self.joined_date).split('-')[0])

    # En Chile se calcula la Indeminización por Años Servicio (IAS) desde el séptimo mes

    # Para calcular el monto de esta indemnización, deben seguirse las siguientes reglas:

    # - Se emplea como base de cálculo, lo pagado en razón de 30 días de la última remuneración mensual devengada 
    # con un tope de 90UF. Esto cuenta como "un mes de remuneración", para efecto de este cálculo.
    #
    # - Se paga un mes de remuneración por cada año de servicio, o fracción superior a los seis meses. 
    # Por ejemplo, si el trabajador suma tres años y ocho meses de servicios, se le pagan en total lo 
    # equivalente a cuatro años, esto es, cuatro meses de indemnización.
    #
    # - El máximo de indemnización que la ley obliga a pagar, es de 11 meses (es decir, por 11 añoos de servicios). 
    # Sin embargo, los trabajadores que tendrán contrato anterior a la entrada en vigencia del actual 
    # Código del Trabajo (es decir, en el año 1981), no están afectos a esta limitación.
    #
    # - Se paga una indemnización mayor, en caso de que ésta haya sido convenida en un contrato individual o colectivo. 
    # Pero la ley prohíbe acordar en un contrato (individual o colectivo) que se pagará una indemnización 
    # menor al cálculo anterior.
    #
    # - Para efectos del cálculo se debe tomar Sueldo Base del último mes + Gratificación y se debe 
    # agregar toda regalía o prestación en especie, sólo cabe atender a si la misma es avaluable en dinero, 
    # sin que sea necesario, por ende, que las partes le hayan fijado un valor en el contrato 

        # TODO considerar si ha trabajado 6+ meses
        if worked_years < 1:

            self.write({
                'state': 'draft'})

            worked_years = int(datetime.datetime.now().year) - int(str(self.joined_date).split('-')[0])
            self.worked_years = worked_years

            raise exceptions.except_orm(_('Employee Working Period is less than 1 Year'),
                                        _('Only an Employee with minimum 1 year of working, will get the Gratuity'))
        else:

            worked_years = int(datetime.datetime.now().year) - int(str(self.joined_date).split('-')[0])
            self.worked_years = worked_years

            cr = self._cr  # find out the correct  date of last salary of  employee

            # TODO Incluir todos los conceptos de Nómina relevantes para la IAS
            query = """select amount from hr_payslip_line psl 
                       inner join hr_payslip ps on ps.id=psl.slip_id
                       where ps.employee_id="""+str(self.employee_name.employee_id.id)+\
                       """and ps.state='done' and psl.code='HAB'
                       order by ps.date_from desc limit 1"""

            cr.execute(query)
            data = cr.fetchall()
            if data :
                 last_salary = data[0][0]
            else :
                last_salary = 0
            self.last_month_salary = last_salary

            # TODO Comparar el salario con el tope de 90 UF
            amount = ((self.last_month_salary + int(self.allowance)) * int(worked_years) * 1) / 1
            self.gratuity_amount = round(amount) if self.state == 'approve' else 0

            self.write({
                'state': 'validate'})

    def approve_function(self):

        if not self.allowance.isdigit():
            raise ValidationError(_('Allowance value should be numeric !!'))

        self.write({
            'state': 'approve'
        })

        amount = ((self.last_month_salary + int(self.allowance)) * int(self.worked_years) * 1) / 1
        self.gratuity_amount = round(amount) if self.state == 'approve' else 0

    def cancel_function(self):
        self.write({
            'state': 'cancel'
        })

    def draft_function(self):
        self.write({
            'state': 'draft'
        })

    # assigning the join date of the selected employee
    @api.onchange('employee_name')
    def _on_change_employee_name(self):
        rec = self.env['hr.resignation'].search([['id', '=', self.employee_name.id]])
        if rec:
            self.joined_date = rec.joined_date
        else:
            self.joined_date = ''
