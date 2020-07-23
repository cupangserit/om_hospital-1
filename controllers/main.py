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