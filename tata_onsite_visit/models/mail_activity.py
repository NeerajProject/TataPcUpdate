
from odoo import api, fields, models, _


class TataVisitTracker(models.Model):
    _name = 'tata.visit.tracker'
    status_time = fields.Char()
    lead_id = fields.Many2one("crm.lead",string='Lead')
    user_id = fields.Many2one("res.users",string="User")
    partner_id = fields.Many2one("res.partner",related="lead_id.partner_id" ,store=True)
    planned_lead = fields.Date(string="Planned Date")
    check_in_date = fields.Datetime(string="Check In")
    check_out_date = fields.Datetime(string="Check out")
    status = fields.Selection([('draft', 'Draft'), ('checkin', 'Check In'),('checkout', 'Check Out'),('cancel', 'Cancel')], readonly=1,string='Status',default='draft')
    time_status = fields.Char(compute="_compute_time_status",string="")



    @api.depends('planned_lead','status')
    def _compute_time_status(self):
        today_date = fields.Date.today()
        print(today_date)
        # print( self.planned_lead )
        for rec in  self:
            if str(today_date) == str(rec.planned_lead) and rec.status in ['draft','checkin']:
                rec.time_status = 'Today'
                rec.status_time = "Today"
            elif (today_date > rec.planned_lead and rec.status in ['draft','checkin']):
                rec.time_status ='Overdue'
                rec.status_time = "Overdue"

            elif (today_date < rec.planned_lead and rec.status in ['draft', 'checkin']):
                rec.time_status = 'Upcoming'
                rec.status_time = "Upcoming"

            else:
                rec.status_time = "Completed"

                rec.time_status = 'Completed'
    def action_action_checkin(self):
        self.check_in_date = fields.Datetime.now()
        self.status = 'checkin'

    def action_action_checkout(self):
        self.check_out_date = fields.Datetime.now()
        self.status = 'checkout'
    def action_action_cancel(self):
        self.status = 'cancel'


class TataVisitTrackerWizard(models.TransientModel):
    _name = 'tata.visit.tracker.wizard'
    lead_id = fields.Many2one("crm.lead",string='Lead',readonly=1)
    user_id = fields.Many2one("res.users",string="User", readonly=1)
    partner_id = fields.Many2one("res.partner",related="lead_id.partner_id")
    planned_date = fields.Datetime(string="Planned Date",required=True)


    def schedule_visits(self):
        self.env['tata.visit.tracker'].create({
    'lead_id': self.lead_id.id,
    'user_id':self.user_id.id,
    'planned_lead': self.planned_date



        }


        )

class CrmLead(models.Model):
    _inherit='crm.lead'

    def action_create_visit(self):
        return {'type': 'ir.actions.act_window',
                'name': _('VISITS'),
                'res_model': 'tata.visit.tracker.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id,
                            'default_user_id': self.env.user.id
                            },
                }

    def action_of_vists(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('VISITS'),
            'res_model': 'tata.visit.tracker',
            'view_mode': 'kanban,tree,form',
            'domain': [('lead_id', '=', self.id),('status','in',['draft','checkin'])],
        }


