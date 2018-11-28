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
    resignation_id = fields.Many2one('hr.resignation', string='Solicitud de Término')
    joined_date = fields.Date(string="Joined Date")
    settle_date = fields.Date(string="Settlement Date") #, default=fields.Date.today())
    worked_years = fields.Integer(string="Total Work Years")
    worked_months = fields.Integer(string="Total Work Months")
    worked_days = fields.Integer(string="Total Work Days")
    notice_days = fields.Integer(string="Days of Notice before termination")
    notice_fact = fields.Float(string="Fracción de pago Aviso Previo")
    last_month_salary = fields.Float(string="Last Salary")
    last_2_month_salary = fields.Float(string="2nd Last Salary ")
    last_3_month_salary = fields.Float(string="3rd Last Salary ")
    average_salary = fields.Float(string="Average Salary (past 3 months)")
    valor_uf = fields.Float(string="Valor UF")
    dias_vaca_pend = fields.Float(string="Días de Vacaciones Pendientes")
    dias_vaca_prop = fields.Float(string="Días Feriado Proporcional")
    allowance = fields.Float(string="Dearness Allowance", default=0)
    gratuity_amount = fields.Float(string="Gratuity Payable", required=True, default=0, readony=True, help=("Gratuity is calculated based on 							the equation Last salary * Number of years of service"))
    ias_amount = fields.Float(string="Indeminización Años Servicio (IAS)", required=False, readony=True, help=("Gratuity is calculated based on 							the equation Last salary * Number of years of service"))
    iap_amount = fields.Float(string="Indeminización Aviso Previo (IAP)", required=False, readony=True, help=("Pago aviso previo despido 							correspondiente a 30 días"))
    ifp_amount = fields.Float(string="Indeminización Feriado Proporcional", required=False, readony=True, help=("Liquidación de Feriádo Proprcional por Vacaciones pendientes"))

    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)

    reason = fields.Selection([('art159', 'Renuncia Trabajador (Art. 159)'), ('art160', 'Despido Justificado (Art. 160)'), ('art161', 'Despido Injustificado (Art. 161)')], string="Settlement Reason", readony=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    # assigning the sequence for the record
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.settlement')
        return super(FinalSettlements, self).create(vals)

    # Check whether any Settlement request already exists
    @api.onchange('employee_id', 'reason')
    @api.depends('employee_id', 'reason')
    def check_request_existence(self):
        for rec in self:
            if rec.employee_id:
                settlement_request = self.env['hr.settlements'].search([('employee_id', '=', rec.employee_id.id),
                                                                           ('state', 'in', ['draft', 'validate', 'approve'])])
                if settlement_request:

                    raise ValidationError(_('A Settlement request is already processed'
                                                ' for this employee'))

                resignation_obj = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id), ('state', '=', 'approved')])
                if resignation_obj:
                    for resignation in resignation_obj:
                        self.resignation_id = resignation.id
                        self.notice_days = int(resignation.notice_period)
                        self.joined_date = resignation.joined_date
                        self.settle_date = resignation.approved_revealing_date
                        self.reason = resignation.reason


                    self.notice_fact = 0

                    # Aviso de Despido tiene menos de 30 días se paga fracción de IAP
                    if self.notice_days <= 30 and self.notice_days >= 0:
                        self.notice_fact = 1 - ( self.notice_days / 30 )

                    # calculating the years of work by the employee
                    end_date = datetime.strptime(str(self.settle_date.year) + "-" + str(self.settle_date.month) + "-" +str(self.settle_date.day), date_format)
                    start_date = datetime.strptime(str(self.joined_date.year) + "-" + str(self.joined_date.month) + "-" +str(self.joined_date.day), date_format)
                    worked_days = (end_date - start_date).days - 1
                    worked_years = int(round(worked_days / 365))
                    worked_months = int(round(worked_days / 365 * 12))
                    self.worked_years = worked_years
                    self.worked_months = worked_months
                    self.worked_days = worked_days

                    cr = self._cr  # search last 3 salaries of employee from Payslips

                    query = """select amount from hr_payslip_line psl 
                               inner join hr_payslip ps on ps.id=psl.slip_id
                               where ps.employee_id="""+str(rec.employee_id.id)+\
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

                    average_salary = ( last_salary + last_2_salary + last_3_salary ) / ( ls_a + ls_b + ls_c )
                    self.average_salary = average_salary
                    self.last_month_salary = last_salary
                    self.last_2_month_salary = last_2_salary
                    self.last_3_month_salary = last_3_salary

                    # Leemos la UF de los Indiocadores de Previred para la última Nómina
                    cr = self._cr
                    query = """select uf from hr_indicadores hri  
                               inner join hr_payslip ps on ps.indicadores_id=hri.id
                               where ps.employee_id="""+str(rec.employee_id.id)+\
                               """and ps.state='done' 
                               order by ps.date_from desc limit 1"""

                    cr.execute(query)
                    data = cr.fetchall()
                    if data:
                        valor_uf = data[0][0]
                    else:
                        valor_uf = 0

                    self.valor_uf = valor_uf

                    # Convertimos el tope de 90 UF a CLP 
                    tope = self.valor_uf * 90

                    # Si el salario promedio de los 3 meses pasados supera el Tope, tomamos el Tope
                    if self.average_salary > tope:
                        amount_base = tope
                    else:
                        amount_base = self.average_salary

                    # Cálculo IAS = Salario Base * Años
                    if self.worked_years >= 1.0 and  rec.reason == 'art161':
                        amount = amount_base * self.worked_years
                        self.ias_amount = round(amount)
                    else:
                        self.ias_amount = 0

                    # Cálculo IAP = Salario Base * Fracción Días Preaviso
                    if rec.reason != 'art159':
                        amount = amount_base * self.notice_fact
                        self.iap_amount = round(amount) 
                    else:
                        self.iap_amount = 0

                    # Cálculo IFP = Salario Base / 30 * Días Feriado Proporcional
                    if self.dias_vaca_prop > 0:
                        amount = amount_base / 30 * self.dias_vaca_prop
                        self.ifp_amount = round(amount)
                    else:
                        self.ifp_amount = 0


                else:
                    raise exceptions.except_orm(_('No existe Solicitud de Término aprobada para este Empleado'),
                                          _('Se debe crear y aprobar una Solcitud de Término para poder calcular Finiquito'))


    @api.multi
    def validate_function(self):
        # Determine previous notice days (from Resignation form)
        resignation_obj = self.env['hr.resignation'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'approved')])
        if resignation_obj:
            for resignation in resignation_obj:
                self.resignation_id = resignation.id
                self.notice_days = int(resignation.notice_period)
                self.joined_date = resignation.joined_date
                self.settle_date = resignation.approved_revealing_date
                self.reason = resignation.reason

            self.notice_fact = 0

            # Aviso de Despido tiene menos de 30 días se paga fracción de IAP
            if self.notice_days <= 30 and self.notice_days >= 0:
                self.notice_fact = 1 - ( self.notice_days / 30 )

            # calculating the years of work by the employee
            end_date = datetime.strptime(str(self.settle_date.year) + "-" + str(self.settle_date.month) + "-" +str(self.settle_date.day), date_format)
            start_date = datetime.strptime(str(self.joined_date.year) + "-" + str(self.joined_date.month) + "-" +str(self.joined_date.day), date_format)
            worked_days = (end_date - start_date).days - 1
            worked_years = int(round(worked_days / 365))
            worked_months = int(round(worked_days / 365 * 12))
            self.worked_years = worked_years
            self.worked_months = worked_months
            self.worked_days = worked_days

            cr = self._cr  # search last 3 salaries of employee from Payslips

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

            average_salary = ( last_salary + last_2_salary + last_3_salary ) / ( ls_a + ls_b + ls_c )
            self.average_salary = average_salary
            self.last_month_salary = last_salary
            self.last_2_month_salary = last_2_salary
            self.last_3_month_salary = last_3_salary

            # Convertimos el tope de 90 UF a CLP 
            tope = self.valor_uf * 90

            amount_base = 0
            # Si el salario promedio de los 3 meses pasados supera el Tope, tomamos el Tope
            if self.average_salary > tope:
                amount_base = tope
            else:
                amount_base = self.average_salary

            # Cálculo IAS = Salario Base * Años
            if self.worked_years >= 1.0 and  self.reason == 'art161':
                amount = amount_base * self.worked_years
                self.ias_amount = round(amount)
            else:
                self.ias_amount = 0

            # Cálculo IAP = Salario Base * Fracción Días Preaviso
            if self.reason != 'art159':
                amount = amount_base * self.notice_fact
                self.iap_amount = round(amount) 
            else:
                self.iap_amount = 0

            # Cálculo IFP = Salario Base / 30 * Días Feriado Proporcional
            if self.dias_vaca_prop > 0:
                amount = amount_base / 30 * self.dias_vaca_prop
                self.ifp_amount = round(amount)
            else:
                self.ifp_amount = 0

            self.write({
                'state': 'validate'})

        else:
            self.write({
                'state': 'draft'})

            raise exceptions.except_orm(_('No existe Solicitud de Término aprobada para este Empleado'),
                                  _('Se debe crear y aprobar una Solcitud de Término para poder calcular Finiquito'))



    def approve_function(self):
        self.write({
            'state': 'approve'
        })


    def cancel_function(self):
        self.write({
            'state': 'cancel'
        })

    def draft_function(self):
        self.write({
            'state': 'draft'
        })



    #@api.multi
    #def unlink(self):
    #    if any(self.filtered(lambda hr.settlements: hr.settlements.state not in ('draft', 'cancel'))):
    #        raise UserError(_('You cannot delete a Settlement which is not draft or cancelled!'))
    #    return super(FinalSettlements, self).unlink()

