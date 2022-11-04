from odoo import models
import time
from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class TataCRMXlsx(models.TransientModel):
    _name = 'tata.crm.xlsx'

    def action_to_from_xlsx(self):
        print(self)
        data = {        }



        print({
            'type': 'ir.actions.report',
            'data': {'model': 'tata.crm.xlsx',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'Current Stock History',
                     'report_name': 'Current Stock History',
                     },
            'report_type': 'tata_crm_from_to'
        })
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'tata.crm.xlsx',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'Current Stock History',
                     'report_name': 'Current Stock History',
                     },
            'report_type': 'tata_crm_from_to'
        }
    def get_xlsx_report(self, data, response):
        print("yes i am tony")


