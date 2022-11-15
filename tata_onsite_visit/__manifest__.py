{
    'name': 'TATA Visit',
    'summary': "Schedule visit for customer",
    'description': """ Schedule Visit for customer""",
    'version': '15',
    'license': "AGPL-3",
    'depends': ['base','crm','sale_crm','custom_executive_crm_tata'],
    'data': [
'security/ir.model.access.csv',
'views/crm_lead.xml',
'security/tata_visit_tracker.xml',
'views/report_onsite_visit.xml'
    ],


    'assets': {

},


    'installable': True,
    'auto_install': False,
}
