# -*- coding: utf-8 -*-
{
    'name': "Automatic Backup to whatever",

    'summary': """
        Automatic Backup with Automatic Action into S3, Dropbox, SFTP or ownCloud.
    """,

    'description': """""",

    'author': "Andreas Wyrobek",
    'website': "https://www.cytex.cc",

    'category': 'Administration',
    'version': '0.1',
	
	'images': ['images/main_screenshot.png'],

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml'
    ],
    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
}
