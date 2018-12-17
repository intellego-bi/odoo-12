# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2017-TODAY Intellego Business Intelligence S.A.(<http://www.intellego-bi.com>).
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#
#    Original Copyright (c) 2011 Cubic ERP - Teradata SAC. (http://cubicerp.com).
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
{
    'name': 'Chile - Chart of Accounts (MFG)',
    'version': '12.0.1.0.0',
    'summary': """Chilean Chart of Accounts for Manufacturing industries """,
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'category': 'Localization',
    'depends': ['account'],
    'data': [
        'data/account_data.xml',
		'data/account_sequence.xml',
		'data/account_journal.xml',
        'data/account_group_data.xml',
        'data/l10n_cl_chart_data.xml',
        'data/account_tax_data.xml',
        'data/account_chart_template_data.xml',
    ],
}
