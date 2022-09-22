{
    'name': 'TATA Custom Contractors',
    'version': '1.0',
    'summary': '',
    'description': """
    """,
    'depends': ['crm','tata_parvash_customization'],
    'data': [
        'security/contractor_entry.xml',
'security/ir.model.access.csv',
'view/res_contractor.xml',
'view/crm_lead.xml',
        'view/filters_of_meeting.xml',
'view/daily_contractors.xml'

    ],

    'installable': True,
    'auto_install': False,
}
