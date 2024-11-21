from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta
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
    property_id = fields.Many2one('estate.property', string='Property', required=False)
    property_type_id=fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)
    validity = fields.Integer(string='Validity', default=0)
    create_date = fields.Datetime(string="Creation Date", readonly=True, default=fields.Datetime.now)
    deadline=fields.Date(string="Deadline", compute="_compute_date_deadline", year=2024)

    # inverse = "_inverse_date_deadline",
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - date.today()).days
            else:
                offer.validity = 20

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
