# © 2008-2016 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Chile :: Currency Rate Update from SBIF",
    "version": "12.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://camptocamp.com",
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
        "views/res_config_settings.xml",
        "security/rule.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True
}
