from odoo import models, fields


class ResUseer(models.Model):
    _inherit = 'res.users'
    phone_number = fields.Char(string='Phone Number')
    Mobile=fields.Char(string='Mobile Number')
