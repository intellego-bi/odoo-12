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
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
from odoo.tools.translate import _


class Product(models.Model):
    _inherit = 'product.template'

	unidades = fields.Float('N° Unidades', digits=dp.get_precision('Product Unit of Measure'), help="N° Unidades por Paquete de producto", copy=True)
	
	largo = fields.Float('Largo (cm)', digits=dp.get_precision('Product Unit of Measure'), help="Largo del corte en CM", copy=True)
	
	ancho = fields.Float('Ancho (cm)', digits=dp.get_precision('Product Unit of Measure'), help="Ancho del corte en CM", copy=True)
	
	gramaje = fields.Float('Gramaje por m2', digits=dp.get_precision('Product Unit of Measure'), help="Gramos de peso por metro cuadrado", copy=True)
	
	lista = fields.Float('Lista', digits=dp.get_precision('Helios Product Class'), help="?", copy=True)
	
	ns = fields.Float('NS', digits=dp.get_precision('Helios Product Class'), help="?", copy=True)
	
	ecobond = fields.Float('Ecobond', digits=dp.get_precision('Helios Product Class'), help="?", copy=True)
	
	mx = fields.Float('MX', digits=dp.get_precision('Helios Product Class'), help="?", copy=True)

