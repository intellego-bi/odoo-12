# Copyright 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def update_bank_journals(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        ajo = env['account.journal']
        journals = ajo.search([('type', '=', 'bank')])
        cct = env.ref(
            'l10n_cl_account_banking_credit_transfer.chile_credit_transfer')
        if cct:
            journals.write({
                'outbound_payment_method_ids': [(4, cct.id)],
            })
        bct = env.ref(
            'l10n_cl_account_banking_credit_transfer.bci_credit_transfer')
        if bct:
            journals.write({
                'outbound_payment_method_ids': [(4, bct.id)],
            })
    return
