odoo.define('crm_search_easy_widget.search_easy_widget', function (require) {
    "use strict";

    const ControlPanel = require('web.ControlPanel');
    const { patch } = require('web.utils');

    const { useState } = owl.hooks;

    patch(ControlPanel.prototype, 'crm_search_easy_widget.search_easy_widget', {

        setup() {
            this._super(...arguments);
        },

        search_based_on_date(e)
        {
        console.log(e)
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
        console.log(action)
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



               },

        download_databased_xlsx_report()
        {
        alert("download_databased_xlsx_report")
          var from_date = $('.tata_from_date_crm_123').val()
        var to_date = $('.tata_to_date_crm_123').val()
        var rpc = require('web.rpc');

          rpc.query({
                model: 'crm.xlsx.report',
                method: 'call_date_based_filters',
                args: [[],from_date,to_date],
            })



        },
        download_summary_xlsx_report()
        {
        alert('download_summary_xlsx_report')
        }
    });

    patch(ControlPanel, 'crm_search_easy_widget.search_easy_widget', {
        template: 'web.Legacy.ControlPanel',
        components: {
            ...ControlPanel.components,
        },
    });
});
