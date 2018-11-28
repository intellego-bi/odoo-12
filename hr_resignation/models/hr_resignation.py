# -*- coding: utf-8 -*-
import datetime
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
date_format = "%Y-%m-%d"


class HrResignation(models.Model):
    _name = 'hr.resignation'
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    def _get_employee_id(self):
        # assigning the related employee of the logged in user
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", default=_get_employee_id,
                                  help='Name of the employee for whom the request is creating')
    department_id = fields.Many2one('hr.department', string="Department", related='employee_id.department_id',
                                    help='Department of the employee')
    joined_date = fields.Date(string="Join Date", help='Joining date of the employee')
    expected_revealing_date = fields.Date(string="Revealing Date", required=True,
                                          help='Date on which he is revealing from the company')
    resign_confirm_date = fields.Date(string="Resign confirm date", help='Date on which the request is confirmed')
    approved_revealing_date = fields.Date(string="Approved Date", help='The date approved for the revealing')
    term_reason = fields.Text(string="Reason", help='Specify reason for leaving the company')
    reason = fields.Selection([('art159', 'Renuncia Trabajador (Art. 159)'), ('art160', 'Despido Justificado (Art. 160)'), ('art161', 'Despido Injustificado (Art. 161)')], string="Settlement Reason", required="True")
    notice_period = fields.Char(string="Notice Period", compute='_notice_period')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Cancel')],
                             string='Status', default='draft')

    @api.onchange('employee_id', 'state')
    @api.depends('employee_id', 'state')
    def set_join_date(self):
        self.joined_date = self.employee_id.joining_date if self.employee_id.joining_date else ''
        if not self.employee_id.joining_date:
            raise ValidationError(_('Actualice la Fehca de Vinculación en el'
                          ' maestro de Empleados y vuelva a generar la solicitud'))

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.resignation') or _('New')
        res = super(HrResignation, self).create(vals)
        return res

    @api.constrains('employee_id')
    def check_employee(self):
        # Checking whether the user is creating leave request of his/her own
        for rec in self:
            if not self.env.user.has_group('hr.group_hr_user'):
                if rec.employee_id.user_id.id and rec.employee_id.user_id.id != self.env.uid:
                    raise ValidationError(_('You cannot create request for other employees'))

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def check_request_existence(self):
        # Check whether any resignation request already exists
        for rec in self:
            if rec.employee_id:
                #resignation_request = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id),
                #                                                         ('state', 'in', ['confirm', 'approved'])])
                resignation_request = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id),
                                                                         ('state', 'in', ['payslip'])])
                if resignation_request:
                    raise ValidationError(_('There is a resignation request in confirmed or'
                                            ' approved state for this employee'))

    @api.multi
    def _notice_period(self):
        # calculating the notice period for the employee
        for rec in self:
            if rec.approved_revealing_date and rec.resign_confirm_date:
                approved_date = datetime.strptime(str(rec.approved_revealing_date), date_format)
                confirmed_date = datetime.strptime(str(rec.resign_confirm_date), date_format)
                notice_period = approved_date - confirmed_date
                rec.notice_period = notice_period.days

    @api.constrains('joined_date', 'expected_revealing_date')
    def _check_dates(self):
        # validating the entered dates
        for rec in self:
            resignation_request = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id),
                                                                     ('state', 'in', ['confirm', 'approved'])])
            if resignation_request:
                raise ValidationError(_('There is a resignation request in confirmed or'
                                        ' approved state for this employee'))
            if rec.joined_date >= rec.expected_revealing_date:
                raise ValidationError(_('Error: Revealing date cannot be before Joining Date'))

    @api.multi
    def confirm_resignation(self):
        for rec in self:
            rec.state = 'confirm'
            rec.resign_confirm_date = str(datetime.now())
            if not rec.employee_id.joining_date:
                raise ValidationError(_('Actualice la Fehca de Vinculación en el'
                              ' maestro de Empleados y vuelva a generar la solicitud'))

    @api.multi
    def cancel_resignation(self):
        for rec in self:
            rec.state = 'cancel'

    @api.multi
    def reject_resignation(self):
        for rec in self:
            rec.state = 'rejected'

    @api.multi
    def approve_resignation(self):
        for rec in self:
            if not rec.approved_revealing_date:
                raise ValidationError(_('Enter Approved Revealing Date'))
            if rec.approved_revealing_date and rec.resign_confirm_date:
                if rec.approved_revealing_date <= rec.resign_confirm_date:
                    raise ValidationError(_('Approved Revealing Date must be before Confirmed Date'))
                rec.state = 'approved'




