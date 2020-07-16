# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

# class for inherit function in another module
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals_list):
        res= super(ResPartner, self).create(vals_list)
        print ('Function Overrided')
        return  res

class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name= fields.Char('Patient Name')

class HospitalPatient(models.Model):
    # define name of table
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    #for constrains
    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age<=5:
                raise ValidationError(_('The Age Must be Greater than 5'))

    #for compute field
    @api.depends('age_group')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age<18:
                    rec.age_group='minor'
                else:
                    rec.age_group='major'

    #action object smart button
    @api.multi
    def open_patient_appointment(self):
        return {
            'name':_('Appointments'),
            'domain':[('patient_id','=',self.id)],
            'view_type':'form',
            'res_model':'hospital.appointment',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',
        }

    def get_appointment_count(self):
        count =self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count= count

    # define field of patient
    name = fields.Char('Contact Number')
    name_seq = fields.Char('Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('trans', 'Transgender')
    ], 'Gender', default='male')
    age_group = fields.Selection([
        ('major','Major'),
        ('minor', 'Minor')
    ], 'Age Group', compute='set_age_group')
    patient_name = fields.Char('Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='always')
    notes = fields.Text('Registration Notes')
    image = fields.Binary('Image', attachment=True)
    #add counting number smartbutton
    appointment_count= fields.Integer('Appointment', compute='get_appointment_count')
    active =fields.Boolean('Active', default=True)




    # Name sequence number otomatis
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New'))==_('New'):
            vals['name_seq']=self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient,self).create(vals)
        return result

