from odoo import fields, models, api

class ResFirm(models.Model):
    _name = 'res.firm'
    name = fields.Char(string="Firm")



class TataMeeting(models.Model):
    _name = 'tata.meeting'

    name = fields.Char(string="Name",required=True)
    place_id = fields.Char('res.place',required=True)
    date = fields.Date(string="Date of Meeting")
    contract_ids = fields.Many2many('res.contractors')
    leads_count = fields.Integer('Leads Count', compute='_compute_leads_count')

    def action_view_opportunity(self):
        action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_opportunities')
        action['domain'] = [('tata_meeting_id', '=', self.id)]
        return action

    def _compute_leads_count(self):
        lead_data = self.env['crm.lead'].search([('tata_meeting_id', '=', self.id)])
        for rec in self:
            rec.leads_count = len(lead_data)


class ResContractors(models.Model):
    _name ='res.contractors'
    name = fields.Char(string='Name',required=True)
    place_id = fields.Many2one('res.place',string='Place')
    mobile = fields.Char(string='Mobile',required=True )
    firm_id = fields.Many2one('res.firm')
    leads_count = fields.Integer('Leads Count', compute='_compute_leads_count')
    meet_count = fields.Integer('Leads Count', compute='_compute_meet_count')

    _sql_constraints = [
        ('mobile', 'unique(mobile)', 'Mobile Number  already exists!')
    ]

    def action_view_opportunity(self):
        action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_opportunities')
        action['domain'] = [('contractor_id', '=', self.id)]
        return action

    def _compute_leads_count(self):
        lead_data = self.env['crm.lead'].search([('contractor_id', '=', self.id)])
        for rec in self:
            rec.leads_count = len(lead_data)

    def action_view_meet_attended(self):
        action = self.env['ir.actions.act_window']._for_xml_id('tata_contractors_custom.tata_meeting_act_window')
        action['domain'] = [('contract_ids', 'in', self.id)]
        return action

    def _compute_meet_count(self):
        lead_data = self.env['tata.meeting'].search([('contract_ids', 'in', self.id)])
        for rec in self:
            rec.meet_count = len(lead_data)