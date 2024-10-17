from  datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order='best_price desc'

    _sql_constraints = [
        ('check_price', 'CHECK(selling_price >= 0)',
         'The percentage of an analytic distribution should be between 0 and 100.')
    ]


    name = fields.Char(default="Unknown")
    desc = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    active = fields.Boolean(string="Active", default=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation', selection=[
        ('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')
    ])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('offer_recieved', 'Offer Recieved'),
        ('offer_accepted', 'Offer Accepted'),
        ('cancelled', 'Cancelled'),
        ('sold', 'Sold'),
    ], default='draft')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_line_id = fields.Many2one('estate.property.line', string='Property Line')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tags_id = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.Many2many('estate.property.offer', string='Offers')
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()
    create_date = fields.Datetime(string="Creation Date", readonly=True, index=True)

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("You cannot mark a cancelled property as sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot mark a sold property as cancelled.")
            record.state = 'cancelled'


    def action_offer_received(self):
        for record in self:
            record.state = 'offer_received'

    def action_offer_accepted(self):
        for record in self:
            record.state = 'offer_accepted'


    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False


    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = (record.date_deadline - record.create_date).days
                record.validity = max(delta, 0)
            else:
                record.validity = 7


    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)


    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden_area(self):
            if self.garden==True:
             self.garden_area=10
             self.garden_orientation='north'
            else:
                self.garden_area=0
                self.garden_orientation=False



    # @api.constrains('selling_price', 'expected_price', 'offer_ids', 'tags_id', 'property_type_id')
    # def _check_price(self):
    #     for record in self:
    #         if record.selling_price <= 0:
    #             raise ValidationError("Selling Price must be a positive value")
    #
    #         if record.expected_price <= 0:
    #             raise ValidationError("Expected Price must be a positive value")
    #
    #         for offer in record.offer_ids:
    #             if offer.price <= 0:
    #                 raise ValidationError("Offer Price must be a positive value")
    #
    #         if record.tags_id:
    #             existing_tags = self.search_count([('tags_id', '=', record.tags_id.id)])
    #             if existing_tags > 1:
    #                 raise ValidationError("Tag must be a unique value")
    #
    #         if record.property_type_id:
    #             existing_types = self.search_count([('property_type_id', '=', record.property_type_id.id)])
    #             if existing_types > 1:
    #                 raise ValidationError("Property Type must be a unique value")
