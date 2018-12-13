# -*- coding: utf-8 -*-
###################################################################################
#
#    © 2008-2016 Camptocamp
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
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
    "name": "Chile - Currency Rate Update",
    'summary': 'Updates Chilean currency rates (USD, EUR, UF and UTM) from SBIF',
    "version": "12.0.1.0.0",
    "author": "Intellego-BI.com, Camptocamp, Odoo Community Association (OCA)",
    "website": "https://www.Intellego-BI.com",
    'maintainer': 'Intellego-BI.com',
    "license": "AGPL-3",
    "category": "Financial Management/Configuration",
    "depends": [
        "base",
        "mail",
        "currency_rate_inverted",  # Added to ensure CLP is inverted
        "account",  # Added to ensure account security groups are present
    ],
    "data": [
        "data/cron.xml",
        "data/res_currency.xml",
        "views/currency_rate_update.xml",
        "views/res_config_settings_api.xml",
        "views/res_config_settings.xml",
        "security/rule.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True
}
