from datetime import timedelta
from odoo import models,fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description='Estate Property Tags'
    _order='name'

    name=fields.Char(string='Name')
    color = fields.Integer(string='Color')
