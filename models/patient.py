from odoo import fields, models, api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'

    patient_name = fields.Char('Name', required=True)
    patient_age = fields.Integer('Age')
    notes = fields.Text('Notes')
    image = fields.Binary('Image')