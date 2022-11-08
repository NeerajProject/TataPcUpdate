from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'



    def check_user_dealer_group(self):
        user = self.env.user
        print("user",user)
        return  user.has_group('custom_executive_crm_tata.group_tata_dealer_salesman')


    def check_current_userp(self):
        user = self.env.user
        return  user.id
