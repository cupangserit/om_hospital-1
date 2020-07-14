from odoo import fields, models, api, _

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
    name_seq = fields.Char('Name Seq', required=True, copy=False, readonly=True,
                           index=True, default=lambda  self: _('New'))


    # Name sequence number otomatis
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New'))==_('New'):
            vals['name_seq']=self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient,self).create(vals)
        return result

