from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    asset_prefix = fields.Char(string="Asset Prefix")
    enable_asset_tracking = fields.Boolean(string="Enable Asset Tracking")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        # Fetch values from system parameters
        res.update({
            'asset_prefix': self.env['ir.config_parameter'].sudo().get_param('assets.asset_prefix', default=''),
            'enable_asset_tracking': self.env['ir.config_parameter'].sudo().get_param('assets.enable_asset_tracking', default=False),
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # Save values to system parameters
        self.env['ir.config_parameter'].sudo().set_param('assets.asset_prefix', self.asset_prefix)
        self.env['ir.config_parameter'].sudo().set_param('assets.enable_asset_tracking', self.enable_asset_tracking)
