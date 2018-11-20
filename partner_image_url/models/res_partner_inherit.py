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
import base64
import requests
import io
from PIL import Image
from odoo import models, fields, api, _
from odoo.exceptions import Warning

class HrEmployeeDocument(models.Model):
    _inherit = ['res.partner']

    web_url = fields.Char(string='Image URL', help='Automatically sanitized HTML contents', copy=False)

    @api.onchange('web_url')
    def onchange_image(self):
        link = self.web_url
        try:
            if link:
                req = requests.get(link).content #, allow_redirects=True, stream=True)
                if req.status_code == 200: 
                    profile_image = base64.b64encode(req)
                    val = {'image': profile_image,}
                    return {'value': val}
#                if req.status_code != 200:
#				    raise Warning("No response from URL")
        except:
            raise Warning("Please provide correct URL or check your image size.!")


			
			
			

#class HrEmployeeDocument(models.Model):
#    _inherit = ['res.partner']
#    web_url = fields.Char(string='Image URL', help='Provide URL for HTML-based image', copy=False)
	
#    @api.onchange('web_url')
#    def onchange_image(self):
#        link = self.web_url
#        try:
#            if link:
#				profile_image = self.base64.b64encode(requests.get(link).content)
#                val = {
#                    'image': profile_image,
#                }
#                return {'value': val}
#        except:
#            raise Warning("Please provide a valid URL and/or verifiy image size.!")