{
    'name': 'Tata Executive Customization',
    'version': '15.0.1.0.0',
    'summary': 'Tata Executive Customization',
    'description': 'Tata Executive Customization',
    'category': 'Extra Tools',
    'depends': ['sales_team','crm',
        'tata_parvash_customization','base','tata_contractors_custom'

    ],
    'data': [
    'security/sale_team.xml',
    # 'security/crm_lead.xml',
    'views/sale_team.xml',
    'views/res_users.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
