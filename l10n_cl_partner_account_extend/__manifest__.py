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
    'name': 'Chile :: Campos Adicionales Partner',
    'summary': """Extiende vistas de módulos Contabilidad y Contactos""",
    'version': '12.0.1.0.0',
    'description': """Búsqueda por RUT, Monto a Pagar y a Cobrar y otros""",
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://www.Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'category': 'Accounting',
    'depends': ['base', 'crm', 'website', 'hr', 'account_accountant', 'stock', 'purchase', 'mrp', 'sale_management', 'quality_control', 'documents', 'mail', 'web_studio', 'maintenance', 'fleet'],
    'license': 'LGPL-3',
    'data': [
        'views/res_partner_account_extend.xml',
        'views/res_account_account_extend.xml',
        'views/cl_accounting_menu.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
