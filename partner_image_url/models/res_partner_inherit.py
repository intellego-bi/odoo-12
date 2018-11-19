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
import requests
import base64
import io
#from PIL import Image
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class Partner(models.Model):
    _inherit = ['res.partner']
    web_url = fields.Char(string='Image URL', help='Provide URL for HTML-based image', copy=False)

	def get_as_base64(url):
        return base64.b64encode(requests.get(url).content)
	
    @api.onchange('web_url')
    def onchange_image(self):
        link = self.web_url
        try:
            if link:
       
                #img_data = requests.get(link).content
                #with open('image_name.jpg', 'wb') as handler:
                #    handler.write(img_data)
				
                #image = open('image_name.jpg', 'rb')
				#open binary file in read mode 
                #image_read = image.read()
                #profile_image = base64.encodestring(image_read)
				profile_image = self.get_as_base64(link)
                val = {
                    'image': profile_image,
                }
                return {'value': val}
        except:
            raise Warning("Please provide a valid URL and/or verifiy image size.!")

			