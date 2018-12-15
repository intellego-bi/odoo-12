.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Currency Rate Update (SBIF Chile)
=================================

Base module to download exchange rates automatically from the SBIF API for Chilean currencies (UF, UTM, USD and EUR).

This module is a fork from the original OCA module *(currency_rate_update)* that downloads exchange rates automatically from *European Central Bank (ECB)* service (ported by Grzegorz Grzelak - OpenGLOBE.pl)

The functionality from the original OCA Module has been replaced and repurposed in order to retrieve exchange rates relating to Chilean Peso (CLP) from API (Web Service) provided by SBIF Chile (https://api.sbif.cl)  The service that retrieves rates from the ECB has been removed from this fork. 

Configuration
=============

Installing this module will create two additional currencies for Chile: *UF (Unidad de Fomento)* and *UTM (Unidad Tributaria Mensual)*. It will also set the position of the symbols and decimal places. 

This module must be used jointly with the OCA module *"Currency Rate Inverted"* which is used in order to set CLP as an *"Inverted Rate Currency"*. You must manually set *"CLP"* as an *"Inverted Rate Currency"* after installing this module. 

**WARNING:** This module must not be deployed on live production systems as it modifies the logic for saving amounts in parallel and local currencies in the Odoo database. Doing so may generate permanent and irreversible damage to data in your database. It is intended for fresh development or greenfield production installations only.  

To configure the module, follow the configuration instructions published for OCA module *"Currency Rate Update"* and the steps outlined here. 


Installation
============

Download and install *"currency_rate_inverted"* and *"l10n_cl_currency_rate_update"* and deploy to your *"addons"* folder on your Odoo server. Installing *"l10n_cl_currency_rate_update"* will also install *"currency_rate_inverted"*. After installing both modules follow these steps:

* Go to *Accounting > Settings > Currencies*
* Edit *CLP* currency and activate *"Inverted Currency Rate"* for this currency *only*
* Go to the SBIF website and follow the process to request your own API Key (https://api.sbif.cl/uso-de-api-key.html)
* Once you have your new API Key (mail reply from SBIF takes a couple of minutes at most), in Odoo, go to *Accounting > General Settings* and scroll down until you find the setting for *Chilean Currency Update*
* Enter your *API Key* in the provided field and *SAVE* your settings
* Go to *Accounting > Settings* and select menu item *"Actualizar Tipos de Cambio SBIF"*
* Press *"Create"* to enter new settings for SBIF web service
* Select *"SBIF Web Service"* and enter parameters as described for original *"currency_rate_update"* module
* Select currencies to update: *USD, EUR, UF and/or UTM* as per your requirements and *SAVE*
* Press *"Actualizar Ahora"* and after a couple of seconds you should see the new exchange rates updated from SBIF

A *cron job* is automatically created and scheduled to run 24 hours after this first execution. You may alter these settings for periodic update by activating *Developer Mode* in Odoo and then in *Settings > Technical > Scheduled Actions* you can configure the cron job parameters as per your needs. It is recommended to run the update everyday during the morning. This will retrieve the currency rates for the previous day from SBIF. If you want to run it immediately, use the button *Run Manually* or go to the menu item created in *Accounting > Settings* and press *"Actualizar Ahora"*.


Known Issues
============

Issues:

* Cronjob will run on weekends and holidays when there is no valid response from SBIF web service. This is logged as an Error/Warning, without further consequences for the update process. 

* Set a *Max Delta Days* of 6 or more days in order to cover longer holidays in Chile (Fiestas Patrias, mainly). 


Further Development
===================

* No further development is planned. 

* The original structure of the *"currency_rate_update"* module on which this is based has been preserved to the best of our abilities so (hopefuly) this Chilean module may be backported into the original OCA module and added as another *Currency Rate Update Service* provider there. 



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

The original *"Currency Rate Update"* module is maintained by the OCA. To contribute to the original module, please visit https://odoo-community.org. OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.


This is a fork of that model **excusively for Chilean specific currency rates** using the SBIF API. Chilean version developed and maintaind by Intellego-BI.com (Santiago, Chile).

.. image:: https://i2.wp.com/intellego-bi.com/ws/wp-content/uploads/2016/05/Intellego-BI-112x35.jpg
   :alt: Intellego-BI.com (Chile)
   :target: https://intellego-bi.com

Intellego-BI.com is a private consultancy based in Santiago, Chile. 

Sharing is caring!

