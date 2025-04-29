# -*- coding: utf-8 -*-
# models/roomtypes.py

from odoo import models, fields, api

class RoomTypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel Room Types'
    # Added _order based on common practice/examples
    _order = "name" 

    name = fields.Char("Room Type", required=True)
    description = fields.Char("Room Type Description")
    # Renamed fields slightly to match examples, kept max dimensions
    room_image = fields.Image("Room Photo", max_width=1024, max_height=1024) 
    bathroom_image = fields.Image("Bathroom Photo", max_width=1024, max_height=1024)

    # Existing One2many field for rooms (from Ex 9)
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')

    # ADDED: One2many field for daily charges (from Ex 8)
    dailycharges_ids = fields.One2many('hotel.dailycharges', 'roomtype_id', string='Daily Charges')