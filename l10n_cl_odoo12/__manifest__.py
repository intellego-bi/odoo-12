# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2018 Intellego-BI.com (https://intellego-bi.com).

{
    'name': 'Chile - Accounting Odoo 12',
    'version': '12.0',
    'description': """
Chilean accounting chart and tax localization - Odoo 12
=======================================================
Plan contable chileno para Odoo 12 

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
