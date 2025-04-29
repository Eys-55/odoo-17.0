# -*- coding: utf-8 -*-
{
    'name': "Hotel Management", # Your module name

    'summary': """
        Manage Hotel Operations including Guests, Rooms, and Registrations""", # Your module summary

    'description': """
        A comprehensive module to manage various aspects of a hotel including:
        - Guest Information Management
        - Room Types and Room Details
        - Guest Registration and Stay Tracking
        - Charges Master List
    """,

    'author': "Your Name/Company", # Your Author Name
    'website': "https://www.yourwebsite.com", # Your Website

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Hotel',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # Add views in logical order (master data first, then transactions)
        'views/mainmenu.xml',
        'views/charges.xml',
        'views/roomtypes.xml',
        'views/rooms.xml',
        'views/guests.xml',
        'views/guestregistration.xml', # Added Guest Registration View
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml', # If you have demo data
    ],
    'installable': True,
    'application': True, # Make it appear as an Application in Odoo Apps
    'auto_install': False,
}