# -*- coding: utf-8 -*-
{
    'name': "hotel",

    'summary': "Hotel Management System",

    'description': """
        Hotel Guest Registration and Billing System.
        Manages Room Types, Rooms, Guests, Charges, and potentially Bookings.
    """,

    'author': "ROYTEK",
    'website': "https://www.yourcompany.com", # Replace with actual website if available

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list (adjust version 16.0 as needed)
    'category': 'Services/Hotel', # Changed category for better classification
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # Security first
        'security/ir.model.access.csv',
        # Then views/data
        'views/mainmenu.xml',
        'views/charges.xml',
        'views/roomtypes.xml', # Added
        'views/rooms.xml',     # Added
        'views/guests.xml',    # Added
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml', # You might add demo data later
    ],
    'installable': True,
    'application': True, # Make it show as an App
    'auto_install': False,
    'license': 'LGPL-3', # Specify a license
}