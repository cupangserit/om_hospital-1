# -*- coding: utf-8 -*-
import pytz

from odoo import  fields, models, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    def test_recordset(self):
        for rec in self:
            #print('Odoo ORM : recordset Operation')
            #search
            partnerts= self.env['res.partner'].search([])
            #mapped
            print ('Partner mapped,...', partnerts.mapped('name'))
            #sorted reverse to descending
            print('Partner, Sorted...', partnerts.sorted(lambda o: o.create_date, reverse=True))
            #filteres
            print('Partner, Filtered...', partnerts.filtered(lambda o: o.customer))

    def delete_lines(self):
        for rec in self:
            print("Time in UTC" ,rec.appointment_datetime)
            usr_tx = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            date_today= pytz.utc.localize(rec.appointment_datetime).astimezone(usr_tx)
            print("Time in Local Timezone ..", date_today)
            rec.appointment_lines = [(5,0,0)]

    def orm_odoo1(self):
        #search all
        hpatients = self.env['hospital.patient'].search([])
        print('Patients All :', hpatients)
        # search female
        female_patients = self.env['hospital.patient'].search([('gender','=','female')])
        print('Female Patients :', female_patients)

        # search with and
        male = self.env['hospital.patient'].search([('gender', '=', 'male'),
                                                    ('patient_age', '>=',30)])
        print('MAle Patients :', male)

        # search witch or
        male_or = self.env['hospital.patient'].search(['|',('gender', '=', 'male'),
                                                    ('patient_age', '>=', 30)])
        print('MaleOr30 Patients :', male_or)

        # search count
        patient_count = self.env['hospital.patient'].search_count([])
        print('count Patients :', patient_count)
        #ref in from odoo import api, fields, models
        patient_ref=self.env.ref('om_hospital.patient_xyz')
        print('Patient Ref :',patient_ref.patient_name)
        # browse
        browse_patient= self.env['hospital.patient'].browse(6)
        if browse_patient.exists():
            print('Browse exist :', browse_patient)
        else:
            print('Not Exists')

        vals = {
            'patient_name':'Mukidi02',
            'patient_age':59,
            'email_id':'mukidioriginal@gmail.com'

        }
        #created_record=self.env['hospital.patient'].create(vals)
        #print('Created Record, :', created_record.id)

        # edit patient
        rec2update= self.env['hospital.patient'].browse(16)
        if rec2update.exists():
            vals ={
                'name':'081910562212',
                'patient_age':48,
                'email_id':'mukidi@gmail.com'

            }
            rec2update.write(vals)
        # duplicate record
        # dup_patient = self.env['hospital.patient'].browse(16)
        # dup_patient.copy()

        # delete
        del_patient= self.env['hospital.patient'].browse([19,20])
        del_patient.unlink()
        print('deleted' , del_patient)

        # orm2
        for rec in self:
            patient = self.env['hospital.patient'].search([('id','=',16)])
            print("Contact : ", patient.name)
            print("Number : ", patient.name_seq)
            print("patient name : ", patient.patient_name)
            print("patient age : ", patient.patient_age)
            print("Gender : ", patient.gender)
        filter_patient = self.env['hospital.patient'].search([]).filtered(lambda s: s.gender == 'trans')
        print('patient filtered : ', filter_patient)
        mapped_patient = self.env['hospital.patient'].search([]).sorted(key='patient_age').mapped('patient_name')
        print('patient mapped name : ', mapped_patient)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect':{
                    'fadeout':'slow',
                    'message':'Appointment Confirm ... Thanks you',
                    'type':'rainbow_man'
                }
            }
    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_success('Appointment')

    def action_done(self):
        for rec in self:
            self.state = 'done'

    #namesequence
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print('test write function')
        return res

    @api.onchange('partner_id')
    def onchange_method(self):
        for rec in self:
            return {'domain':{'order_id':[('partner_id','=',rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        # appointment_lines= [(5,0,0)]
        # product_rec = self.env['product.product'].search([])
        # for pro in product_rec:
        #     line = (0,0, {
        #         'product_id':pro.id,
        #         'product_qty':1,
        #     })
        #     appointment_lines.append(line)
        # res.update({
        #     'appointment_lines':appointment_lines,
        #     'patient_id':1,
        #     #'notes':'Patient BPJS Maksimal 3 Hari 3 Malam'
        # })
        res['patient_id']=1
        return res

    #defaultvaluenote
    def _get_default_note(self):
        return 'Patient BPJS Maksimal 3 Hari 3 Malam'
    name= fields.Char('Appointment ID', required=True, copy=False, readOnly=True, index=True, default=lambda self: _('New'))
    patient_id=fields.Many2one('hospital.patient',string='Patient ID', required=True)
    doctor_id= fields.Many2one('hospital.doctor','Doctor')
    doctor_ids= fields.Many2many('hospital.doctor','hospital_patient_rel','appointment_id','doctor_id' ,string='Doctors', )

    patient_age=fields.Integer('Age' , related='patient_id.patient_age')
    notes=fields.Text('Registration Notes', default=_get_default_note)
    doctor_notes = fields.Text('Notes', default=_get_default_note)
    pharmacy_notes = fields.Text('Notes', default=_get_default_note)
    appointment_date= fields.Date('Date', required=True )
    appointment_date_end = fields.Date('End Date')
    appointment_lines= fields.One2many('hospital.appointment.lines','appointment_id', 'Appointment Lines')
    appointment_datetime = fields.Datetime('Date Time')
    partner_id = fields.Many2one('res.partner', 'Customer')
    order_id = fields.Many2one('sale.order', 'Sales Order')
    product_id= fields.Many2one('product.template', 'Product Template')
    amount= fields.Float('Total Ammount')
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'cancel'),
    ], 'Status', readonly=True, default='draft')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            lines =[(5,0,0)]
            #lines =[]
            for line in self.product_id.product_variant_ids:
                val = {
                    'product_id': line.id,
                    'product_qty':5
                }
                lines.append((0,0, val))
            rec.appointment_lines=lines

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product','Medicine')
    product_qty = fields.Integer('Quantity')
    appointment_id= fields.Many2one('hospital.appointment', string="Appointment ID")
    sequence = fields.Integer('No')
    appointment_id=fields.Many2one('hospital.appointment','Appointment ID')
