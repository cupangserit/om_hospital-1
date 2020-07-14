from odoo import fields, models, api

class HospitalPatient(models.Model):
    # define name of table
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    # define field of patient
    patient_name = fields.Char('Name', required=True)
    patient_age = fields.Integer('Age')
    notes = fields.Text('Notes')
    image = fields.Binary('Image')
    name = fields.Char('Test')

