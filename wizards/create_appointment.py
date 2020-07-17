from odoo import models, fields

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment'

    patient_id= fields.Many2one('hospital.patient', 'Patient')
    appointment_date= fields.Date('Date')