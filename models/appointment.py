# -*- coding: utf-8 -*-
from odoo import  fields, models, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    def action_confirm(self):
        for rec in self:
            self.state = 'confirm'

    def action_done(self):
        for rec in self:
            self.state = 'done'

    #namesequence
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    #defaultvaluenote
    def _get_default_note(self):
        return 'Patient BPJS Maksimal 3 Hari 3 Malam'
    name= fields.Char('Appointment ID', required=True, copy=False, readOnly=True, index=True, default=lambda self: _('New'))
    patient_id=fields.Many2one('hospital.patient',string='Patient ID', required=True)
    patient_age=fields.Integer('Age' , related='patient_id.patient_age')
    notes=fields.Text('Registration Notes', default=_get_default_note)
    doctor_notes = fields.Text('Notes', default=_get_default_note)
    pharmacy_notes = fields.Text('Notes', default=_get_default_note)
    appointment_date= fields.Date('Date', required=True)

    state = fields.Selection([
        ('draft','Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'cancel'),
    ], 'Status', readonly=True, default='draft')