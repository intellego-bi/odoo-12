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
{
    'name': 'Chile :: Financial Accounting Legal Statements',
    'summary': """Legal Reporting and Financial Statements for Chile/IFRS Accounting""",
    'version': '12.0.1.0.0',
    'description': """Statutary Reporting and Financial Statements for Chilean Localization""",
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://www.Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'category': 'Accounting',
    'depends': ['l10n_cl_coa', 'account_reports'],
    'license': 'LGPL-3',
    'data': [
        'data/account_financial_html_report_data.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
