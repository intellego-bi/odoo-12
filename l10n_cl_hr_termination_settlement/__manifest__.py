# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2018-TODAY Intellego Business Intelligence S.A.
#    (<http://www.intellego-bi.com>)
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#
#    Forked from a part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
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
####################################################################################
{
    'name': 'Chile - RRHH :: Employee Termination Settlement',
    'version': '12.0.1.0.0',
    'summary': """Employee Termination and Final Settlement  """,
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'category': 'Human Resources',
    'depends': ['base', 'l10n_cl_hr_termination_request', 'mail', 'hr_payroll'],
    'data': ['views/hr_chile_menus.xml',
             #'views/employee_gratuity_view.xml',
             'views/gratuity_sequence.xml',
             'views/final_settlements.xml',
             'data/salary_rule_settle.xml',
             'security/ir.model.access.csv'],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
