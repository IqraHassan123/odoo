from odoo import fields, models, api


class Attribute(models.Model):
    _name = 'ad.attribute'
    _description = 'Asset Attribute'

    title = fields.Char(string='Title', required=True)
    value = fields.Char(string='Value', required=True)
    asset_ids = fields.Many2many('assets.handling', 'ad_asset_attributes_rel', 'attribute_id', 'asset_id', string='Assets')
