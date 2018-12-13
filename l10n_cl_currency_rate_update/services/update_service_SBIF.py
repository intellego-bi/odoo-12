# © 2009 Camptocamp
# © 2009 Grzegorz Grzelak
# © 2018 Intellego-BI.com
# © 2018 Rodolfo Bermudez Neubauer
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import UserError

from .currency_getter_interface import CurrencyGetterInterface

from datetime import datetime
from lxml import etree
from datetime import date, timedelta

import logging
_logger = logging.getLogger(__name__)

import requests
import xmltodict as xm

apikey = '067edb08cf9ceb0b212d83a0bc8baf39816f026a'
sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/?apikey=' + apikey + '&formato=xml'
rep = requests.get(sbifurl, allow_redirects=True)
fecha_ayer = date.today() - timedelta(1)
fecha = fecha_ayer.strftime('%Y-%m-%d')


class SBIFGetter(CurrencyGetterInterface):
    """Implementation of Currency_getter_factory interface
    for SBIF service
    """
    code = 'SBIF'
    name = 'SBIF Chile'
    supported_currency_array = ["USD", "EUR", "UF", "UTM"]

    el1 = ''
    el2 = ''
    #fecha = datetime.today().strftime('%Y-%m-%d')
    fecha_ayer = date.today() - timedelta(5)
    fecha = fecha_ayer.strftime('%Y-%m-%d')
    #raise UserError(
    #                _('Hoy = (%s) y Ayer = (%s)') % (fecha, fecha_ayer))

    #def rate_retrieve(self, dom, ns, curr, sbif_api_key):
    def rate_retrieve(self, curr, sbif_api_key):
        """Parse XML to retrieve currencies data
        """
        mensaje = " "
        if len(sbif_api_key) > 1:
            apikey = sbif_api_key
        else:
            raise UserError(
                _('Falta configurar API Key en Ajustes Generales de Contabilidad en Odoo'))

        fecha_ayer = date.today() - timedelta(1)
        fecha = fecha_ayer.strftime('%Y-%m-%d')
        ano = str(fecha_ayer.year)
        mes = str(fecha_ayer.month)
        dia = str(fecha_ayer.day)

        sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/' + ano + '/' + mes + '/dias/' + dia + '?apikey=' + apikey + '&formato=xml'
        #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/?apikey=' + apikey + '&formato=xml'

        req = requests.get(sbifurl, allow_redirects=True)

        if req.status_code == 200:
            docs = xm.parse(req.content)
            fecha = docs['IndicadoresFinancieros']['Dolares']['Dolar']['Fecha']
        else:
            docs = xm.parse(req.content)
            mensaje = docs['ErrorAPI-SBIF']['Mensaje']
            raise UserError(
                _('Error: %s') % mensaje)

        res = {}
        el1 = '''Dolares'''
        el2 = '''Dolar'''
        #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/?apikey=' + apikey + '&formato=xml'
        sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/' + ano + '/' + mes + '/dias/' + dia + '?apikey=' + apikey + '&formato=xml'
        valor = '1,0'
        if curr == 'USD':
           #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/?apikey=' + apikey + '&formato=xml'
           sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/dolar/' + ano + '/' + mes + '/dias/' + dia + '?apikey=' + apikey + '&formato=xml'
           el1 = '''Dolares'''
           el2 = '''Dolar'''

        if curr == 'UF':
           #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/uf/?apikey=' + apikey + '&formato=xml'
           sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/uf/' + ano + '/' + mes + '/dias/' + dia + '?apikey=' + apikey + '&formato=xml'
           el1 = '''UFs'''
           el2 = '''UF'''

        if curr == 'UTM':
           #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/utm/?apikey=' + apikey + '&formato=xml'
           sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/utm/' + ano + '/' + mes + '?apikey=' + apikey + '&formato=xml'
           el1 = '''UTMs'''
           el2 = '''UTM'''

        if curr == 'EUR':
           #sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/euro/?apikey=' + apikey + '&formato=xml'
           sbifurl = 'https://api.sbif.cl/api-sbifv3/recursos_api/euro/' + ano + '/' + mes + '/dias/' + dia + '?apikey=' + apikey + '&formato=xml'
           el1 = '''Euros'''
           el2 = '''Euro'''

        rep = requests.get(sbifurl, allow_redirects=True)
        docu = xm.parse(rep.content)

        if rep.status_code != 200:
            mensaje = docu['ErrorAPI-SBIF']['Mensaje']
            raise UserError(
                _('Error: %s') % mensaje)

        fecha = docu['IndicadoresFinancieros'][el1][el2]['Fecha']
        valor = docu['IndicadoresFinancieros'][el1][el2]['Valor']

        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

        res['rate_currency'] = float(valor)

        return res

    def get_updated_currency(self, currency_array, main_currency,
                             max_delta_days, sbif_api_key):
        """implementation of abstract method of Curreny_getter_interface"""
        url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        # Important : as explained on the SBIF web site, the currencies are
        # at the beginning of the morning ; so, until 10 a.m. SCL time
        # the currency rates are the ones of trading day N-1

        fecha_ayer = date.today() - timedelta(1)
        fecha = fecha_ayer.strftime('%Y-%m-%d')
        dia = str(fecha_ayer.day)

        # We do not want to update the main currency
        if main_currency in currency_array:
            currency_array.remove(main_currency)

        _logger.debug("SBIF currency rate service : connecting...")

        _logger.debug("SBIF sent a valid XML file")


        rate_date = fecha
        # Don't use DEFAULT_SERVER_DATE_FORMAT here, because it's
        # the format of the XML of SBIF, not the format of Odoo server !
        rate_date_datetime = datetime.strptime(rate_date, '%Y-%m-%d')
        self.check_rate_date(rate_date_datetime, max_delta_days)
        # We dynamically update supported currencies
        self.supported_currency_array.append('CLP')
        _logger.debug("Supported currencies = %s " %
                      self.supported_currency_array)
        self.validate_cur(main_currency)

        if len(sbif_api_key) < 1:
            raise UserError(
                _('Falta configurar API Key en Ajustes Generales de Contabilidad en Odoo'))

        if main_currency == 'CLP':
            main_curr_data = self.rate_retrieve(main_currency, sbif_api_key)

        for curr in currency_array:
            self.validate_cur(curr)
            if curr == 'CLP':
                 rate = 1

            else:
                curr_data = self.rate_retrieve(curr, sbif_api_key)
                rate = curr_data['rate_currency']

            self.updated_currency[curr] = rate

            _logger.debug("Rate retrieved : 1 %s = %s %s" % (main_currency, rate, curr))
        return self.updated_currency, self.log_info
