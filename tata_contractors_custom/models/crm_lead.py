from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    mobile = fields.Char(required=True)
    _sql_constraints = [
        ('mobile', 'unique(mobile)', 'Mobile Number  already exists!')
    ]
class CrmLead(models.Model):
    _inherit ='crm.lead'
    based_on_contract = fields.Boolean()
    tata_meeting_id = fields.Many2one('tata.meeting', String="Contractor Meet")
    contractor_id = fields.Many2one('res.contractors', String="Contractors")
    @api.onchange('based_on_contract')
    def set_team_is_null(self):
        self.ensure_one()
        if self.based_on_contract:
            self.user_id = self.env.ref('tata_contractors_custom.user_contractor_lead').id
            self.team_id = self.env.ref('tata_contractors_custom.team_contractor_lead').id
        else:
            self.user_id = self.env.user.id
    @api.onchange('tata_meeting_id')
    def set_domain_contractors(self):
        self.ensure_one()
        return {'domain': {'contractor_id': [('id', 'in',self.tata_meeting_id.contract_ids.mapped('id')) ]}}


