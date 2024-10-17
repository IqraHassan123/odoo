from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order='name'
    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')  # Reference the Many2one field


class EstatePropertyLine(models.Model):
    _name = 'estate.property.line'
    _description = 'Estate Property Line'

    name = fields.Char(string='Name', required=True)
    property_id = fields.Many2one('estate.property', string='Property')