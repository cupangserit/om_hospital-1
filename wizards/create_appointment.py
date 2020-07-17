from odoo import models, fields

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment'

    patient_id= fields.Many2one('hospital.patient', 'Patient')
    appointment_date= fields.Date('Date')

    def create_appointment(self):
        vals= {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Create From the Wizard/Code'
        }
        self.env['hospital.appointment'].create(vals)