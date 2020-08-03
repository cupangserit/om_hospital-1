from odoo import  http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth='public', website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res= super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print('Hospital Patient Controller inherit')
        return res

class AppointmentController(http.Controller):

    @http.route('/om_hospital/appointments', auth='user', type='json')
    def appointment_bannder(self):
        return  {
            'html':"""
                <div class='o_onboarding o_onboarding_wrap'>
                    <center>
                            <img width='1920px' height='192' src='/om_hospital/static/src/img/hospital.jpg'/>
                    </center>
                </div>
            """
        }

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

