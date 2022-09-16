from odoo import fields, models, api,_



class ResUser(models.Model):
    _inherit = 'res.users'
    is_executive = fields.Boolean()

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    assigned_id = fields.Many2one('res.users' ,tracking =1)

    def sent_invitation_throw_whatsapp(self):
        return {
                'name': _(' Whatsapp Message'),
                'view_mode': 'form',
                'res_model': 'whats.app.message',
                'view_id': self.env.ref('tata_whatsapp_integration.whats_app_message_form').id,
                'type': 'ir.actions.act_window',
                'context': {
                    'default_lead_id': self.id,
                    'default_partner_id': self.partner_id.id,
                            'default_mobile': self.partner_id.mobile,
                            'default_message_string': 'Thank you for contacting Tata Steel Pravesh! Please let us know how we can help you.'
                            },
                'target': 'new'
            }
    def sent_assigned_message(self):
        return {
                'name': _(' Whatsapp Message'),
                'view_mode': 'form',
                'res_model': 'whats.app.assigned',
                'view_id': self.env.ref('tata_whatsapp_integration.whats_app_assigned_form').id,
                'type': 'ir.actions.act_window',
                'context': {
                            'default_lead_id': self.id

                            },
                'target': 'new'
            }


