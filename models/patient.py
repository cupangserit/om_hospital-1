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

    @api.multi
    def action_confirm(self):
        print("inherit function sale order working")
        res = super(SalesOrderInherit, self).action_confirm()
        return res

    patient_name = fields.Char(string='Patient Name')
    is_patient = fields.Boolean(string='Is Patient')

class ResPartner(models.Model):
    _inherit = 'res.partner'
    company_type= fields.Selection(selection_add=[('patient','Patient')])
    #gender = fields.Selection(selection_add=[('transgender', 'Transgender')])

class HospitalPatient(models.Model):
    # define name of table
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    def action_patients(self):
        #print('test patient server action')
        return {
            'name':_('Patient Server Action'),
            'domain':[],
            'view_type':'form',
            'res_model':'hospital.patient',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window'
        }

    @api.multi
    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)

    @api.multi
    def print_report_excel(self):
        return self.env.ref('om_hospital.report_patient_card_xls').report_action(self)

    #call cron job
    @api.multi
    def test_cron_job(self):
        print('Test Cron')
        #code to execute cron

    @api.multi
    def name_get(self):
        res =[]
        for rec in self:
            res.append((rec.id, '%s - %s' %(rec.name_seq, rec.patient_name)))
        return res

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

    #get counting number
    def get_appointment_count(self):
        count =self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
        self.appointment_count= count

    #onchange doctor ang get gender
    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

        # Sending Email in Button Click
    # https://www.youtube.com/watch?v=CZVRmtv6re0&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=44
    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

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
    ], 'Age Group', compute='set_age_group',)
    #], 'Age Group', compute='set_age_group', store=True) by pass comput field
    patient_name = fields.Char('Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='always', group_operator=False)
    patient_age2 = fields.Float('Age2')
    notes = fields.Text('Registration Notes')
    image = fields.Binary('Image', attachment=True)
    #add counting number smartbutton
    appointment_count= fields.Integer('Appointment', compute='get_appointment_count')
    active =fields.Boolean('Active', default=True)
    doctor_id=fields.Many2one('hospital.doctor', 'Doctor')
    email_id=fields.Char('Email')
    user_id=fields.Many2one('res.users', 'PRO')
    doctor_gender= fields.Selection([
        ('male','Male'),
        ('female', 'Female')
    ], string='Doctor Gender')
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')


    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper= rec.patient_name.upper() if rec.patient_name else False

    @api.depends('patient_name')
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    # Name sequence number otomatis
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New'))==_('New'):
            vals['name_seq']=self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient,self).create(vals)
        return result

