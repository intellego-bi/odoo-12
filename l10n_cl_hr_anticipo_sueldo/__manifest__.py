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
    'name': 'RRHH Chile - Solicitud de Anticipo de Sueldo',
    'version': '12.0.1.1.0',
    'summary': 'Permite a los empleados solicitar anticipo de remuneraciones',
    'description': """
        Ayuda a tratar solicitudes puntuales para pago anticipado y el flujo de trabajo asociado.
        """,
    'category': 'Human Resources',
    'author': 'Intellego-BI.com',
    'company': 'Intellego-BI.com',
    'website': 'https://www.Intellego-BI.com',
    'maintainer': 'Intellego-BI.com',
    'depends': [
        'hr_payroll', 'hr', 'account', 'hr_contract', 'l10n_cl_hr', 'l10n_cl_hr_prestamo', 
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/hr_anticipo_reglas_salariales.xml',
        'data/hr_anticipo_sueldo_sequence.xml',
        'views/hr_anticipo_sueldo.xml',
        'views/hr_salary_structure.xml',
        'views/hr_anticipo_sueldo_menu.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

