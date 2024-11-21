from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order='name'
    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')  # Reference the Many2one field
    sequence=fields.Integer(string='Sequence', default=10)
    tags_id=fields.Many2many('estate.property.tags', string='estate_property_tags')
    offer_ids=fields.One2many('estate.property.offer', 'price', string='Offers')
    offer_count=fields.Integer(string='Offer Count', compute='_compute_offer_count')

    @api.depends('property_ids')
    def _compute_offer_count(self):
        print("=============>", self.property_ids)
        final_count = 0
        for property in self.property_ids:
            print(property)
            final_count += len(property.offer_ids)

        self.offer_count = final_count

class EstatePropertyLine(models.Model):
    _name = 'estate.property.line'
    _description = 'Estate Property Line'

    name = fields.Char(string='Name', required=True)
    property_id = fields.Many2one('estate.property', string='Property')

