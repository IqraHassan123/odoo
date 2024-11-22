from odoo import fields, models, api, exceptions

class AssetsHandling(models.Model):
    _name = 'assets.handling'
    _description = 'Asset Handling'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=False, ondelete='cascade', index=True)
    title = fields.Char(string="Title", required=True)
    asset_id = fields.Char(string='Asset ID', readonly=True)  # Auto-generated
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

    @api.model
    def create(self, vals):
        asset_prefix = self.env['ir.config_parameter'].sudo().get_param('assets.asset_prefix', default='EQP-')
        enable_asset_tracking = self.env['ir.config_parameter'].sudo().get_param('assets.enable_asset_tracking', default=False)

        if not enable_asset_tracking:
            raise exceptions.UserError("Asset Tracking is disabled. Enable it in Asset Settings to create assets.")

        next_number = self.env['ir.sequence'].next_by_code('asset.code.sequence') or '0001'
        vals['asset_id'] = f"{asset_prefix}{next_number}"
        return super(AssetsHandling, self).create(vals)
