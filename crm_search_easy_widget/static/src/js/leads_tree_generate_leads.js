odoo.define('crm_search_easy_widget.search_easy_widget', function (require) {
    "use strict";

    const ControlPanel = require('web.ControlPanel');
    const { patch } = require('web.utils');

    const { useState } = owl.hooks;

    patch(ControlPanel.prototype, 'crm_search_easy_widget.search_easy_widget', {

        setup() {
            this._super(...arguments);

       },


 willStart:  function () {
        var self = this



       this.rpc({
            model: 'crm.lead',
            method: 'check_user_dealer_group',
            args: [[]],
        }).then(function(action) {
        self.is_dealer = action
        console.log("user",action)
        });


       this.rpc({
            model: 'crm.lead',
            method: 'check_current_userp',
            args: [[]],
        }).then(function(action) {
        self.user_id = action
        console.log("user",action)
        });


//alert(self.is_dealer)










       },


        search_based_on_date(e)
        {
        console.log(this)







        if (this.is_dealer)
        {




           e.preventDefault();
        var from_date = $('.tata_from_date_crm_123').val()
        var to_date = $('.tata_to_date_crm_123').val()
        if (to_date && from_date){

        var action= {
                name : 'Leads from '+from_date+ " to "+to_date,
                type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, "kanban"],[false, "list"],[false,"graph"],[false,"pivot"],[false,"form"],[false,'calendar'],[false,'activity']],
            target: 'current',
            domain: [["lead_created_date", ">", from_date],["lead_created_date","<",to_date],['user_id','=',this.user_id]],
            context : {
             'search_default_salesperson': 1 ,
             'search_default_stage': 1



                  }

        }


   return new Promise(resolve => {
                this.env.bus.trigger('do-action', {
                    action,
                    options: {
                        on_close: () => {
                            resolve();
                            this.fetchAndUpdate();
                        },
                    },
                });
            });






        }




























        }
        else{

           e.preventDefault();
        var from_date = $('.tata_from_date_crm_123').val()
        var to_date = $('.tata_to_date_crm_123').val()
        if (to_date && from_date){

        var action= {
                name : 'Leads from '+from_date+ " to "+to_date,
                type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, "kanban"],[false, "list"],[false,"graph"],[false,"pivot"],[false,"form"],[false,'calendar'],[false,'activity']],
            target: 'current',
            domain: [["lead_created_date", ">", from_date],["lead_created_date","<",to_date]],
            context : {
             'search_default_salesperson': 1 ,
             'search_default_stage': 1



                  }

        }


   return new Promise(resolve => {
                this.env.bus.trigger('do-action', {
                    action,
                    options: {
                        on_close: () => {
                            resolve();
                            this.fetchAndUpdate();
                        },
                    },
                });
            });






        }


        }






               },



               tata_my_pipe_line(){
//
                   var action= {
            name : 'Pipeline ',
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, "kanban"],[false, "list"],[false,"graph"],[false,"pivot"],[false,"form"],[false,'calendar'],[false,'activity']],
            target: 'current',
            domain: [['type','=','opportunity']],
            context:{                    'default_type': 'opportunity',
                               'search_default_assigned_to_me': 1            }



        }
//
//
   return new Promise(resolve => {
                this.env.bus.trigger('do-action', {
                    action,
                    options: {
                        on_close: () => {
                            resolve();
                            this.fetchAndUpdate();
                        },
                    },
                });
            });



               },


    });

    patch(ControlPanel, 'crm_search_easy_widget.search_easy_widget', {
        template: 'web.Legacy.ControlPanel',
        components: {
            ...ControlPanel.components,
        },
    });
});