# -*- coding: utf-8 -*-
# models/dailycharges.py

from odoo import models, fields, api

class DailyCharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'Hotel Room Type Daily Charges List'
    _order = 'charge_id' # Optional: Order by charge name

    charge_id = fields.Many2one('hotel.charges', string="Charge Title", required=True)
    amount = fields.Float("Daily Amount", digits=(10, 2), required=True)
    # Inverse field for the One2many relationship in hotel.roomtypes
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type", ondelete='cascade', required=True) 

    # Optional: To display charge description easily if needed
    charge_description = fields.Char(related='charge_id.description', string='Description', readonly=True)