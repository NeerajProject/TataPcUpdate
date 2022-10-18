from odoo import fields, models,api

class ResUsers(models.Model):
    _inherit = 'res.users'
    territory_id = fields.Many2one('res.territory' , string='Territory')
class CrmLead(models.Model):
    _inherit = 'crm.lead'
    phone = fields.Char(related='partner_id.mobile',store=True,readonly=False)



