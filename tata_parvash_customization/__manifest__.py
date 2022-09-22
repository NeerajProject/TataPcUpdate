{
    'name': 'TATA STEEL CUSTOMIZATION',
    'version': '1.0',
    'summary': '',
    'description': """
    """,
    'depends': ['crm','sale','base','sale_crm','stock'],
    'data': [
'security/ir.model.access.csv',
'view/res_partner.xml',
        'view/crm_lead.xml',
        'view/sale_gift.xml',
        'view/stock_picking.xml',
        'view/sale_gift_filter_group.xml'

    ],
    'installable': True,
    'auto_install': False,
}
