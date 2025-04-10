# -*- coding: utf-8 -*-
# models/rooms.py

from odoo import models, fields, api

class Rooms(models.Model):
    _name = 'hotel.rooms'
    _description = "Hotel Rooms"

    name = fields.Char("Room No.", required=True)
    description = fields.Char("Room Description")
    # Consider adding a Many2one link to roomtypes later:
    # room_type_id = fields.Many2one('hotel.roomtypes', string='Room Type')