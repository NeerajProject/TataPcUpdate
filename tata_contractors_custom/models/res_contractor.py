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

class ResContractors(models.Model):
    _name ='res.contractors'
    name = fields.Char(string='Name',required=True)
    place_id = fields.Many2one('res.place',string='Place')
    mobile = fields.Char(string='Mobile',required=True )
    firm_id = fields.Many2one('res.firm')
    _sql_constraints = [
        ('mobile', 'unique(mobile)', 'Mobile Number  already exists!')
    ]