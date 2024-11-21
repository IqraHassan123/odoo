from odoo import fields, models, api

class AssetsHandling(models.Model):
    _name = 'assets.handling'
    _description = 'Asset Handling'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=False, ondelete='cascade', index=True)
    title = fields.Char(string="Title", required=True)
    asset_id = fields.Char(string='Asset ID', required=True)
    serial_number = fields.Char(string='Serial Number')
    category_id = fields.Many2one('ad.category', string='Category', required=True)
    condition = fields.Selection([
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished')
    ], string='Condition', required=True)
    assigned_by_id = fields.Many2one('hr.employee', string='Assigned By', required=True)
    assigned_to = fields.Many2one('hr.employee', string='Assigned To', required=True)
    authorized_by_id = fields.Many2one('hr.employee', string='Authorized By', required=True)
    purchased_date = fields.Date(string='Purchased Date', required=True)
    purchased_amount = fields.Float(string='Purchased Amount', required=True)
    summary = fields.Text(string='Summary', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='pending')
    attribute_ids = fields.Many2many('ad.attribute', 'ad_asset_attributes_rel', 'asset_id', 'attribute_id', string='Attributes')
    supervisor_id = fields.Many2one('hr.employee', string='Supervisor')
    Assets = fields.Selection([('received', 'Received'), ('submitted', 'Submitted')])
    user_id = fields.Many2one('res.users', string='User')
