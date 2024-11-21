from odoo import fields, models, api


class AssetFileAttachment(models.Model):
    _name = 'ad.fileattachment'
    _description = 'Asset File Attachment'

    url = fields.Char(string='URL', required=True)
    asset_id = fields.Many2one('assets.handling', string='Asset', required=True)
