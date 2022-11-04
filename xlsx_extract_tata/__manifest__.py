{
    'name': 'TATA XLSX EXTRACT',
    'summary': "Xlsx report based on day,weekly,monthly basis",
    'description': """ This module will help admin to see the login details
            of user like date, country, state and city""",
    'version': '15',
    'license': "AGPL-3",
    'depends': ['base','crm','tata_whatsapp_integration'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_xlsx_report.xml'
    ],

'assets': {
        'web.assets_backend': [
            'xlsx_extract_tata/static/src/js/action_manager.js',
        ],
    },

    'installable': True,
    'auto_install': False,
}
