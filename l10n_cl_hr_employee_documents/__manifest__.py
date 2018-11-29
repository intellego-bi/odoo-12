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
    'name': 'RRHH Chile - Documentos para Empleados',
    'version': '12.0.1.0.0',
    'summary': """Permite gestionar documentación asociada a empleados controlando su Fecha de Vencimiento mediante notificaciones en Odoo.""",
    'description': """Documentación anexa para Empleados con gestión de venicmiento vía notificaciones.""",
    'category': 'Human Resources',
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://www.Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_documents_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
