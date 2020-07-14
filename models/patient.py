from odoo import fields, models, api, _

class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name= fields.Char('Patient Name')

class HospitalPatient(models.Model):
    # define name of table
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'


    # define field of patient
    name = fields.Char('Test')
    name_seq = fields.Char('Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('trans', 'Transgender')
    ], 'Gender', default='male')
    patient_name = fields.Char('Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='onchange')
    notes = fields.Text('Registration Notes')
    image = fields.Binary('Image', attachment=True)





    # Name sequence number otomatis
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New'))==_('New'):
            vals['name_seq']=self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient,self).create(vals)
        return result

