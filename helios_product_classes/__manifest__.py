# -*- encoding: utf-8 -*-
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
    'name': 'Helios Product Attributes',
    'version': '12.0',
    'description': """
Atributos de Productos para Helios.
====================================

    - Agrega atributos a vista de productos
    
    """,
    'license': 'AGPL-3',
    'category': 'Warehouse',
    'author': 'Rodolfo Bermúdez Neubauer',
    'website': 'https://www.intellego-BI.com',
    'depends': [
        'stock'
    ],
    'data': [
        'data/helios_product_classes_decimal_precision.xml',
        'views/helios_product_classes_view.xml'		
    ],
   
    'installable': True,
    'auto_install': False,
}
