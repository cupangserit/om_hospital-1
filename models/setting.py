from odoo import api, fields, models , _


class HospitalSettings(models.TransientModel):
    _inherit = "res.config.settings"

    note = fields.Char('Note')

    @api.model
    def get_values(self):
        res= super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('om_hospital.note')
        res.update(
            notes=notes
        )
        return res

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('om_hospital.note', self.note)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('om_hospital.note')
        res.update(
            note=notes
        )
        return res


