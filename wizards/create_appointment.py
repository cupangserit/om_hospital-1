from odoo import models, fields

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment'

    patient_id= fields.Many2one('hospital.patient', 'Patient', ondelete="cascade")
    appointment_date= fields.Date('Date')

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    def create_appointment(self):
        vals= {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Create From the Wizard/Code'
        }
        self.patient_id.message_post(body="appointment berhasil dibuat", subject="Appointment")
        self.env['hospital.appointment'].create(vals)

    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print('Appointment', rec.name)
        return {
            'type':"ir.actions.do_nothing"
        }