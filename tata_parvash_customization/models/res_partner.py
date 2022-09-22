from odoo import api, fields, models

class ResPlace(models.Model):
    _name ="res.place"
    name = fields.Char(string='Place')

class ResProjectType(models.Model):
    _name='res.project.type'
    name = fields.Char(string='Name')


class ProductLineCrm(models.Model):
    _name='product.line.crm'
    product_id = fields.Many2one('product.product' ,string="Product")
    booking_id = fields.Char(string="Booking Id")
    date_of_booking = fields.Date(string="Date of Booking")
    product_uom_qty = fields.Float(string="Unit")
    unit_id = fields.Many2one('uom.uom' ,string="Unit")
    crm_lead_id = fields.Many2one('crm.lead')


class ResTerritory(models.Model):
    _name = 'res.territory'
    name = fields.Char(string='Name')


class ResPartner(models.Model):
    _inherit = 'res.partner'
    agent_type = fields.Selection([('local', 'Local'), ('distributor', 'Distributor'), ('agent', 'Agent')], string='Type')
    territory_id = fields.Many2one('res.territory', string='Territory')
    parent_partner = fields.Many2one('res.partner',String="Distributor")


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    house_warming_date = fields.Date(string="Housewarming Date")
    territory_id = fields.Many2one('res.territory', default=lambda self: self.partner_id.territory_id.id )
    product_ids = fields.One2many('product.line.crm','crm_lead_id',String='Product')
    is_new = fields.Boolean(compute ='compute_state')
    is_qualified = fields.Boolean(compute='compute_state')
    is_offered = fields.Boolean(compute='compute_state')
    is_won = fields.Boolean(compute='compute_state')
    project_type = fields.Many2one('res.project.type',string='Project Type')
    project_description = fields.Char(string="Project Description")
    product_categ_id = fields.Many2one('product.category',string="Product Category")
    place_id = fields.Many2one('res.place', string="Place")
    lead_created_date = fields.Date(string="Create Date", default=fields.Date.context_today)
    lead_closed_date = fields.Date(string="Closed Date")




    @api.depends('stage_id')
    def compute_state(self):
        self.is_new = False
        self.is_qualified = False
        self.is_offered = False
        self.is_won = False

        if self.stage_id.id == self.env.ref("crm.stage_lead1").id:
            self.is_new = True
        if self.stage_id.id == self.env.ref("crm.stage_lead2").id:
            self.is_qualified = True
        if self.stage_id.id == self.env.ref("crm.stage_lead3").id:
            self.is_offered = True
        if self.stage_id.id == self.env.ref("crm.stage_lead4").id:
            self.is_won = True

    def action_new_quotation(self):
        product_list = []
        for rec in self.product_ids:
            product_list.append((0,0,{
                'product_id':rec.product_id.id,
                'product_uom':rec.unit_id.id,
                'product_uom_qty':rec.product_uom_qty
            }))
        action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
            'default_order_line': product_list
        }
        if self.team_id:
            action['context']['default_team_id'] = self.team_id.id,
        if self.user_id:
            action['context']['default_user_id'] = self.user_id.id
        return action



class ProductCategory(models.Model):
    _inherit = 'product.category'
    active = fields.Boolean(default=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    state_gift = fields.Selection(related='sale_id.gift_given_id.state')

    def action_done_gift(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("tata_parvash_customization.sale_gift_act_window")
        action['domain'] = [('sale_order', '=', self.sale_id.id)]
        return action


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    categ_id = fields.Many2one('product.category', 'Product Category',default=False, required=True,
                               help="Select category for the current product")


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    gift_given_id = fields.Many2one('sale.gift')
    state_gift = fields.Selection(related = 'gift_given_id.state' ,default=fields.Date.today())

    def action_quotation_send(self):
        if self.opportunity_id:
             temp = super(SaleOrder, self).action_quotation_send()
             self.opportunity_id.stage_id = self.env.ref('crm.stage_lead3').id
             return temp
        else:
            return super(SaleOrder, self).action_quotation_send()

    def action_confirm(self):
        if self.opportunity_id:
            temp = super(SaleOrder, self).action_confirm()
            self.opportunity_id.stage_id = self.env.ref('crm.stage_lead4').id
            if self.gift_given_id:
                pass
            else:
                self.gift_given_id = self.gift_given_id.create({

                    'sale_order': self.id,
                    'state': 'draft'
                })

            return temp
        else:
            return super(SaleOrder, self).action_confirm()

    def action_view_gift(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("tata_parvash_customization.sale_gift_act_window")
        action['domain'] = [('sale_order', '=', self.id)]
        return action


