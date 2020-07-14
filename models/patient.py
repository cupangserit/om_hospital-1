from odoo import fields, models, api

class HospitalPatient(models.Model):
    # define name of table
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _inherit = ['mail.thread','mail.activity.mixin']

    # define field of patient
    patient_name = fields.Char('Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='onchange')
    notes = fields.Text('Notes')
    image = fields.Binary('Image')
    name = fields.Char('Test')

