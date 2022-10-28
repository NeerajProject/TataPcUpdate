# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Lead test',
    'summary': 'Generate Leads/Opportunities based on country, industries, size, etc.',
    'category': 'Sales/CRM',
    'version': '1.2',
    'depends': [
'xlsx_extract_tata'
    ],
    'data': [

    ],
    'auto_install': True,
    'assets': {
        'web.assets_backend': [
            'crm_search_easy_widget/static/src/js/**/*',
        ],
        'web.assets_qweb': [
            'crm_search_easy_widget/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
}
