from odoo import  http
from odoo.http import request

class Hospital(http.Controller):

    @http.route('/hospital/patient', website=True, auth='public')
    def hospital_patient(self, **kw):
        #return "Hospital LobotIjo "
        patients = request.env['hospital.patient'].sudo().search([])
        return http.request.render('om_hospital.patient_page',{
            'patients':patients
        })

    # api to update patient data
    @http.route('/update_patient', type="json", auth="user")
    def update_patient(self,**rec):
        if request.jsonrequest:
            if rec['id']:
                patient = request.env['hospital.patient'].sudo().search([('id','=',rec['id'])])
                if patient:
                    patient.sudo().write(rec)
                args = {'success':True, 'message':'Success'}
        return args


    # building api odoo to get patient
    @http.route('/create_patient',type='json', auth='user')
    def create_patient(self,**rec):
        if request.jsonrequest:
            # print('rec',rec)
            if rec ['name']:
                vals ={
                    'patient_name': rec['name'],
                    'email_id': rec['email_id']
                }
                new_patient = request.env['hospital.patient'].sudo().create(vals)
                args ={'success':True, 'message':'Success', 'ID':new_patient.id}
            return args
    # api to get patient record
    @http.route('/get_patients', type='json', auth='user')
    def get_patients(self):
        patients_rec = request.env['hospital.patient'].search([])
        patients=[]
        for rec in patients_rec:
            vals ={
                "id":rec.id,
                "name": rec.patient_name,
                "age": rec.patient_age,
                "patient_id": rec.name_seq,
            }
            patients.append(vals)
        data ={'status':200, 'response':patients, 'message': 'Success'}
        return data
