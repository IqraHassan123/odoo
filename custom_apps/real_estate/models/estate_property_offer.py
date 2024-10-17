from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order =  'price desc'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', default='pending')

    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    def action_accept(self):
        if self.status != 'pending':
            raise UserError("You can only accept a pending offer.")
        self.write({'status': 'accepted'})
        # Set buyer and selling price in the property
        self.property_id.write({
            'buyer_id': self.partner_id.id,
            'selling_price': self.price,
        })
        return True

    def action_refuse(self):
        if self.status != 'pending':
            raise UserError("You can only refuse a pending offer.")
        self.write({'status': 'refused'})
        return True
