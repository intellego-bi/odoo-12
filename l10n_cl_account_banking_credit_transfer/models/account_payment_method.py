# Copyright 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    pain_version = fields.Selection(selection_add=[
        ('pain.001.chile.001', 'Banco de Chile (v001)'),
        ('pain.016.bci.001', 'BCI (v001)'),
        ])

    @api.multi
    def get_xsd_file_path(self):
        self.ensure_one()
        if self.pain_version in [
                'pain.001.chile.001', 'pain.016.bci.001']:
            path = 'l10n_cl_account_banking_credit_transfer/data/%s.xsd'\
                % self.pain_version
            return path
        return super(AccountPaymentMethod, self).get_xsd_file_path()
