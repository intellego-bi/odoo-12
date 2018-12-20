# Chile - Archivos Planos para Pagos Masivos con Transferencia Bancaria
[l10n_cl_account_banking_credit_transfer]

## Odoo (ERP/CRM)
 - Based on OCA Module "Account Banking SEPA Credit Transfer"
 - Aims to incorporate Chilean Banks for outgoing payments bank transfers
 - Sadly, each Chilean Bank has a propiretary file format, so we will adjust the European "Pain" standard for Chilean Banks.
 - First attemps will implement Banco de Chile and Banco BCI

## Scope 
**Features list: Chilean Localization**

    * Use OCA module "Account Payment Order" for payment process and interface

## Credits
<p>
<img width="200" alt="Logo Intellego-BI" src="https://i2.wp.com/intellego-bi.com/ws/wp-content/uploads/2016/05/Intellego-BI-112x35.jpg" />
</p>

**Intellego-BI.com** - https://intellego-bi.com
 - Rodolfo Bermúdez Neubauer <odoo@intellego-bi.com>


## Thanks to
 
 **Odoo Community Association (OCA)** https://odoo-community.org <br>

 ## To do
 
 - Everything... just starting out!

 
 ## Disclaimer
 - Forked from OCA Module 
 - Open source software: use at your own risk. 
 - Public private repository. Not currently supporting third parties


====================================
Account Banking SEPA Credit Transfer
====================================

Module to export payment orders in SEPA XML file format.

SEPA PAIN (PAyment INitiation) is the new european standard for
Customer-to-Bank payment instructions. This module implements SEPA Credit
Transfer (SCT), more specifically PAIN versions 001.001.02, 001.001.03,
001.001.04 and 001.001.05. It is part of the ISO 20022 standard, available on
https://www.iso20022.org.

The Implementation Guidelines for SEPA Credit Transfer published by the
European Payments Council (https://www.europeanpaymentscouncil.eu) use
PAIN version 001.001.03, so it's probably the version of PAIN that you should
try first.

It also includes pain.001.003.03 which is used in Germany instead of 001.001.03.
You can read more about this here (only in german language):
http://www.ebics.de/startseite/

**Table of contents**

.. contents::
   :local:

Installation
============

This module depends on :
* account_banking_pain_base

This module is part of the OCA/bank-payment suite.

Configuration
=============

* Create a Payment Mode dedicated to SEPA Credit Transfer.

* Select the Payment Method *SEPA Credit Transfer to suppliers* (which is
  automatically created upon module installation).

* Check that this payment method uses the proper version of PAIN.

Usage
=====

In the menu *Invoicing/Accounting > Payments > Payment Order*, create a new
payment order and select the Payment Mode dedicated to SEPA Credit
Transfer that you created during the configuration step.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/bank-payment/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/bank-payment/issues/new?body=module:%20account_banking_sepa_credit_transfer%0Aversion:%2012.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Akretion
* Tecnativa

Contributors
~~~~~~~~~~~~

* Alexis de Lattre <alexis.delattre@akretion.com>
* Stéphane Bidoul <stephane.bidoul@acsone.eu>
* Stefan Rijnhart
* Julien Laloux
* Alexandre Fayolle
* Raphaël Valyi
* Erwin van der Ploeg
* Sandy Carter
* `Tecnativa <https://www.tecnativa.com>`__:

  * Antonio Espinosa
  * Pedro M. Baeza

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/bank-payment <https://github.com/OCA/bank-payment/tree/12.0/account_banking_sepa_credit_transfer>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
