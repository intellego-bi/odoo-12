# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2018 Intellego-BI.com (https://intellego-bi.com).

{
    'name': 'Chile :: Chart of Accounts & Taxes - Odoo 12',
    'version': '12.0',
    'description': """
Chilean Chart of Accounts and Tax Localization - Odoo 12
=========================================================
Plan de Cuentas e Impuestos para Chile - Odoo 12 

    """,
    'author': 'Intellego-BI.com',
    'website': 'https://intellego-BI.com',
    'category': 'Localization',
    'depends': ['account'],
    'data': [
        'data/l10n_cl_chart_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
    ],
}
