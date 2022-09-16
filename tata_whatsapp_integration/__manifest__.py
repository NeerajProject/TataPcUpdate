{
    'name': 'Send Whatsapp Message',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'depends': [
        'crm', 'contacts','sale_crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/whats_app_message.xml',
        'views/crm_lead.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
