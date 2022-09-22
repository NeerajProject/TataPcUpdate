from odoo import fields, models, api,_
from odoo.exceptions import AccessError, UserError, ValidationError

from datetime import datetime


class SaleGift(models.Model):
    _name = 'sale.gift'
    state = fields.Selection([('draft', 'Open'), ('sent', 'Closed')], string='State',default='draft')
    partner_id = fields.Many2one(related="sale_order.partner_id" ,store=True)
    sale_order = fields.Many2one('sale.order', string="Sale Order")
    sale_order_name = fields.Char(related='sale_order.name', string="Sequence Number")
    order_date = fields.Datetime(related='sale_order.date_order')
    gift_date = fields.Date(string="Distribution Date")
    housewarming_date = fields.Date(related='sale_order.opportunity_id.house_warming_date' ,store=True)
    note = fields.Html('Description')
    date_of_today = fields.Date(compute='_compute_today_date')
    color = fields.Char('Color', compute='_compute_color_date')


    def _compute_today_date(self):
        for rec in self:
              rec.date_of_today = fields.Date.today()
    def _compute_color_date(self):
        for rec in self:
            if rec.state =='sent':
                rec.color ='present'
            else:
                if rec.date_of_today == rec.housewarming_date:
                    rec.color ='present'
                else:
                    if rec.housewarming_date:
                       if rec.housewarming_date > rec.date_of_today:
                        rec.color ="before"
                       else:
                           rec.color = 'after'
                    else:
                        rec.color ="not_entered"
                    print(rec.housewarming_date)
                    print(rec.date_of_today)

    def action_done(self):
        if self.gift_date:

            self.state = 'sent'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Congratulations! ',
                    'type': 'rainbow_man',
                }
             }
        else:
            raise UserError(
                _('Please to enter the Distribution date'))


