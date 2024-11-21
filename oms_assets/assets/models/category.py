from odoo import models, fields


class Category(models.Model):
    _name = 'ad.category'
    _description = 'Asset Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
