# -*- coding: utf-8 -*-
# models/guestregistration.py

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from datetime import date, timedelta

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Guest Registration and Stay Management'
    _order = 'date_reservation desc, id desc'

    # Basic Info
    name = fields.Char("Registration Reference", readonly=True, required=True, copy=False, default='New')
    guest_id = fields.Many2one('hotel.guests', string="Guest Name", required=True, index=True)
    
    # NEW FIELD: For filtering rooms by type
    filter_roomtype_id = fields.Many2one('hotel.roomtypes', string="Filter by Room Type", index=True)
    
    # UPDATED FIELD: Domain now uses filter_roomtype_id
    room_id = fields.Many2one(
        'hotel.rooms', 
        string="Room No.", 
        required=True, 
        domain="[('roomtype_id', '=', filter_roomtype_id)]", 
        index=True
    )
    
    # Related field still useful for displaying the type of the *selected* room
    roomtype_id = fields.Many2one(related='room_id.roomtype_id', string="Room Type", store=True, readonly=True)

    # Dates
    date_reservation = fields.Date("Reservation Date", default=fields.Date.context_today)
    date_checkin_planned = fields.Date("Planned Check-in", required=True, index=True)
    date_checkout_planned = fields.Date("Planned Check-out", required=True, index=True)
    date_checkin_actual = fields.Date("Actual Check-in", readonly=True)
    date_checkout_actual = fields.Date("Actual Check-out", readonly=True)

    # Computed Field: Duration
    duration_planned = fields.Integer(string="Planned Duration (days)", compute='_compute_duration', store=True)

    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', readonly=True, copy=False, index=True, track_visibility='onchange')

    @api.onchange('filter_roomtype_id')
    def _onchange_filter_roomtype_id(self):
        """ Clear room_id if the filter changes """
        if self.room_id and self.room_id.roomtype_id != self.filter_roomtype_id:
            self.room_id = False
        # Return the updated domain for room_id dynamically (optional but good practice)
        # This ensures the domain updates immediately in the UI without saving
        domain = []
        if self.filter_roomtype_id:
            domain = [('roomtype_id', '=', self.filter_roomtype_id.id)]
        return {'domain': {'room_id': domain}}


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.guestregistration') or 'New'
        # Add basic date validation on create
        if 'date_checkin_planned' in vals and 'date_checkout_planned' in vals:
            if vals['date_checkout_planned'] <= vals['date_checkin_planned']:
                raise exceptions.ValidationError(_("Planned Check-out date must be after Planned Check-in date."))
        result = super(GuestRegistration, self).create(vals)
        # Ensure room type filter matches room on create if filter is set
        if result.filter_roomtype_id and result.room_id.roomtype_id != result.filter_roomtype_id:
             raise exceptions.ValidationError(_("The selected Room does not match the Room Type filter."))
        return result

    def write(self, vals):
        # Add basic date validation on write
        checkin = vals.get('date_checkin_planned', self.date_checkin_planned)
        checkout = vals.get('date_checkout_planned', self.date_checkout_planned)
        if checkin and checkout and checkout <= checkin:
            raise exceptions.ValidationError(_("Planned Check-out date must be after Planned Check-in date."))
        
        res = super(GuestRegistration, self).write(vals)

        # Ensure room type filter matches room on write if relevant fields are changed
        for rec in self:
             if rec.filter_roomtype_id and rec.room_id.roomtype_id != rec.filter_roomtype_id:
                 raise exceptions.ValidationError(_("The selected Room does not match the Room Type filter."))
        return res


    @api.depends('date_checkin_planned', 'date_checkout_planned')
    def _compute_duration(self):
        for reg in self:
            if reg.date_checkin_planned and reg.date_checkout_planned:
                if reg.date_checkout_planned <= reg.date_checkin_planned:
                    reg.duration_planned = 0 
                else:
                    delta = reg.date_checkout_planned - reg.date_checkin_planned
                    reg.duration_planned = delta.days
            else:
                reg.duration_planned = 0

    def _check_schedule_conflict(self):
        """Calls the PostgreSQL function to check for conflicts."""
        self.ensure_one() 
        if not self.room_id or not self.date_checkin_planned or not self.date_checkout_planned:
            raise exceptions.ValidationError(_("Room and planned check-in/check-out dates must be set to check for conflicts."))

        # Check room type consistency before checking schedule
        if self.filter_roomtype_id and self.room_id.roomtype_id != self.filter_roomtype_id:
             raise exceptions.ValidationError(_("The selected Room does not match the Room Type filter. Cannot check schedule."))

        query = "SELECT check_room_schedule_conflict(%s, %s, %s, %s)"
        params = (
            self.room_id.id,
            self.date_checkin_planned,
            self.date_checkout_planned,
            self.id or 0 
        )
        self.env.cr.execute(query, params)
        result = self.env.cr.fetchone()
        if result and result[0]: # If function returns TRUE
            raise exceptions.ValidationError(
                _("Schedule conflict detected for Room %s between %s and %s. Another guest is booked during this time.") %
                (self.room_id.name, self.date_checkin_planned, self.date_checkout_planned)
            )
        # No conflict found if we reach here

    # Button Actions
    def action_reserve(self):
        for rec in self:
            if not rec.guest_id or not rec.room_id or not rec.date_checkin_planned or not rec.date_checkout_planned:
                raise exceptions.UserError(_("Please fill in Guest, Room Type Filter (optional), Room, and Planned Dates before reserving."))
            if rec.date_checkout_planned <= rec.date_checkin_planned:
                raise exceptions.ValidationError(_("Planned Check-out date must be after Planned Check-in date."))
            if rec.filter_roomtype_id and rec.room_id.roomtype_id != rec.filter_roomtype_id:
                raise exceptions.ValidationError(_("The selected Room does not match the Room Type filter."))
            rec._check_schedule_conflict()
            rec.write({'state': 'reserved'})

    def action_checkin(self):
        for rec in self:
            if rec.date_checkout_planned <= rec.date_checkin_planned:
                raise exceptions.ValidationError(_("Planned Check-out date must be after Planned Check-in date."))
            if rec.filter_roomtype_id and rec.room_id.roomtype_id != rec.filter_roomtype_id:
                raise exceptions.ValidationError(_("The selected Room does not match the Room Type filter."))
            rec._check_schedule_conflict()
            rec.write({'state': 'checked_in', 'date_checkin_actual': date.today()})

    def action_checkout(self):
        for rec in self:
            if rec.date_checkin_actual and date.today() < rec.date_checkin_actual:
                raise exceptions.ValidationError(_("Cannot check out before the actual check-in date."))
            rec.write({'state': 'checked_out', 'date_checkout_actual': date.today()})

    def action_cancel(self):
        for rec in self:
            if rec.state not in ['draft', 'reserved', 'checked_in']:
                raise exceptions.UserError(_("Cannot cancel a registration that is already checked out or cancelled."))
            rec.write({'state': 'cancelled', 'date_checkin_actual': None, 'date_checkout_actual': None}) 

    def action_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft', 'date_checkin_actual': None, 'date_checkout_actual': None})