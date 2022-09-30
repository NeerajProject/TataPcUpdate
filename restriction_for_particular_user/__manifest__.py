{
    'name': 'Custom TATA Restriction',
    'version': '1.0',
    'summary': '',
    'description': """
    """,
    'depends': ['crm','sales_team','mail','tata_whatsapp_integration'],
    'data': [
'security/sale_team_restriction.xml',

'security/sales_team_recording_rules.xml',
'security/crm_lead.xml'

    ],
    'assets': {

    },

    'installable': True,
    'auto_install': False,
}
