.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Currency Rate Update (SBIF Chile)
=================================

Base module to download exchange rates automatically from the SBIF API for Chilean currencies (UF, UTM, USD and EUR).

This module is a fork from the original OCA module that downloads exchange rates automatically from European central bank service (ported by Grzegorz Grzelak - OpenGLOBE.pl)

The reference rates are taken from the API provided by SBIF Chile (https://api.sbif.cl) 

Configuration
=============

Installing this module will create two additional currencies for Chile: UF (Unidad de Fomento) and UTM (Unidad Tributaria Mensual).

This module must be used jointly with the OCA module "Currency Rate Inverted" which is used in order to set CLP as an "Inverted Rate Currency". 

To configure the module, follow the configuration instructions for "Currency Rate Update". 

to configure periodic update, activate Developer Mode in Odoo and then, in the menu *Settings > Technical > Scheduled Actions*, make sure that the action *Currency Rate Update* is active. If you want to run it immediately, use the button *Run Manually*.

This module is compatible with OCA module 'currency_rate_inverted' also found in OCA/currency repository, that allows to maintain exchange rates in inverted format, helping to resolve rounding issues.

Usage
=====

The module supports multi-company currency in two ways:

* when currencies are shared, you can set currency update only on one
  company
* when currencies are separated, you can set currency on every company
  separately

A function field lets you know your currency configuration.

If in multi-company mode, the base currency will be the first company's
currency found in database.

Know issues / Roadmap
=====================

Roadmap:

* API Key as a COnfig Parameter
* Correct update from previous day

Credits
=======

Contributors
------------

* Nicolas Bessi <nicolas.bessi@camptocamp.com>
* Jean-Baptiste Aubort <jean-baptiste.aubort@camptocamp.com>
* Joël Grand-Guillaume <joel.grandguillaume@camptocamp.com>
* Grzegorz Grzelak <grzegorz.grzelak@openglobe.pl> (ECB, NBP)
* Vincent Renaville <vincent.renaville@camptocamp.com>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com> (Port to V7)
* Agustin Cruz <openpyme.mx> (BdM)
* Jacque-Etienne Baudoux <je@bcim.be>
* Juan Jose Scarafia <jjscarafia@paintballrosario.com.ar>
* Mathieu Benoi <mathben963@gmail.com>
* Fekete Mihai <feketemihai@gmail.com> (Port to V8)
* Dorin Hongu <dhongu@gmail.com> (BNR)
* Paul McDermott
* Alexis de Lattre <alexis@via.ecp.fr>
* Miku Laitinen
* Assem Bayahi
* Daniel Dico <ddico@oerp.ca> (BOC)
* Dmytro Katyukha <firemage.dima@gmail.com>
* Jesús Ventosinos Mayor <jesus@comunitea.com>
* Rodolfo Bermúdez Neubauer (rbermudez@intellego-bi.com)

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

The original "Currency Rate Update" module is maintained by the OCA. This is a fork of that model for Chilean currencies using the SBIF API.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
