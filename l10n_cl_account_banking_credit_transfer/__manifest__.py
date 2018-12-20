# Copyright 2010-2016 Akretion (www.akretion.com)
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Banking Chile Credit Transfer',
    'summary': 'Create Files for Outgoing Bank Transfers for Chilean Banks',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': "Intellego-Bi.com, "
              "Akretion, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/intellego-bi/odoo-12',
    'category': 'Banking addons',
    'conflicts': ['account_banking_sepa_credit_order'],
    'depends': ['account_payment_order'],
    #'depends': ['account_banking_pain_base'],
    'data': [
        'data/account_payment_method.xml',
    ],
    #'demo': [
    #    'demo/sepa_credit_transfer_demo.xml'
    #],
    'post_init_hook': 'update_bank_journals',
    'installable': True,
}
