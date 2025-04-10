# -*- coding: utf-8 -*-
# models/guests.py

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta # Required for age calculation

class Guests(models.Model):
    _name = 'hotel.guests'
    _description = 'Hotel Guests Information'
    _order = 'lastname, firstname' # Default sorting

    # Direct Fields
    lastname = fields.Char("Lastname", required=True)
    firstname = fields.Char("Firstname", required=True)
    middlename = fields.Char("Middlename")
    address_streetno = fields.Char("Address/ Street & No.")
    address_area = fields.Char("Address / Area,Unit&Bldg,Brgy")
    address_city = fields.Char("Address / City/Town")
    address_province = fields.Char("Address / Province/State")
    zipcode = fields.Char("ZIP Code")
    contactno = fields.Char("Contact No.")
    email = fields.Char("Email")
    gender = fields.Selection([
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('OTHER', 'Other') # Consider adding 'Other' or 'Prefer not to say'
        ], string="Gender")
    birthdate = fields.Date("BirthDate")
    photo = fields.Image("Guest Photo", max_width=1024, max_height=1024)

    # Computed Fields
    name = fields.Char(string='Full Name', compute='_compute_name', store=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True)

    @api.depends('lastname', 'firstname', 'middlename')
    def _compute_name(self):
        for guest in self:
            parts = [guest.lastname, guest.firstname, guest.middlename]
            # Filter out empty parts and join with space, add comma after lastname
            filtered_parts = [part for part in parts if part]
            if len(filtered_parts) > 0:
                name_str = filtered_parts[0] # Lastname
                if len(filtered_parts) > 1:
                    name_str += ", " + " ".join(filtered_parts[1:]) # Firstname Middlename
                guest.name = name_str
            else:
                guest.name = ''


    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for guest in self:
            if guest.birthdate:
                # Calculate age using relativedelta for accuracy
                delta = relativedelta(today, guest.birthdate)
                guest.age = delta.years
            else:
                guest.age = 0