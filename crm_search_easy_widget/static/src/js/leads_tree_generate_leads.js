odoo.define('crm_search_easy_widget.search_easy_widget', function (require) {
    "use strict";

    const ControlPanel = require('web.ControlPanel');
    const { patch } = require('web.utils');

    const { useState } = owl.hooks;

    patch(ControlPanel.prototype, 'crm_search_easy_widget.search_easy_widget', {

        setup() {
            this._super(...arguments);
        },

        search_based_on_date()
        {
        alert("yes my lord namabala")
        },

        download_databased_xlsx_report()
        {
        alert("download_databased_xlsx_report")
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
