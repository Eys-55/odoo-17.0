# -*- coding: utf-8 -*-
# models/roomtypes.py

from odoo import models, fields, api

class RoomTypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel Room Types'

    name = fields.Char("Room Type", required=True)
    description = fields.Char("Room Type Description")
    room_image = fields.Image("Room Photo", max_width=1024, max_height=1024)
    bathroom_image = fields.Image("Bathroom Photo", max_width=1024, max_height=1024)

    # Added One2many field for rooms
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')