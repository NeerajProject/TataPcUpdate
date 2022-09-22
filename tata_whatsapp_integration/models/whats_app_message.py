from odoo import fields, models, api


class WhatsAppMessage(models.TransientModel):
    _name = 'whats.app.message'
    lead_id = fields.Many2one('crm.lead')
    partner_id = fields.Many2one('res.partner')
    mobile = fields.Char()
    message_string = fields.Text(string='Text')

    def send_whatsapp_message(self):
        if self.message_string and self.mobile:
            message_string =  self.message_string
            number = self.partner_id.mobile
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }

            self.lead_id.message_post(body="<p> <strong>"+self.env.user.name + "</strong> sent <strong>WhatsApp message</strong> to <strong> Welcome Message </strong> to Customer  ")
            return send_msg

class WhatsAppMessage(models.TransientModel):
    _name = 'whats.app.assigned'
    lead_id = fields.Many2one('crm.lead')
    user_id = fields.Many2one('res.users',domain=[('is_executive','=',True)])

    def send_whatsapp_message(self):
        print(self.lead_id.place_id)

        if  self.lead_id.place_id:
            message_string =self.lead_id.name + " has been assigned to  You \n"+" Customer : "+self.lead_id.partner_id.name +"\n Phone :"+self.lead_id.partner_id.mobile+"\n Place "+self.lead_id.place_id.name
        else:
            message_string =self.lead_id.name + " has been assigned to  You \n"+" Customer : "+self.lead_id.partner_id.name +"\n Phone :"+self.lead_id.partner_id.mobile


        if message_string and self.user_id.mobile:

            number = self.user_id.mobile
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }
            self.lead_id.assigned_id = self.user_id.id

            self.lead_id.message_post(body="<strong>"+self.env.user.name + "</strong> assigned <strong> "+self.user_id.name+"</strong> to follow the Lead <strong>"    +self.lead_id.name+"</strong>")
            return send_msg