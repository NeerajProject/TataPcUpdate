from odoo import fields, models, api

import time
from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
from xlsxwriter.utility import xl_cell_to_rowcol, xl_range_abs
from odoo.exceptions import AccessError, UserError, ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ResUser(models.Model):
    _inherit = 'res.users'
    is_executive = fields.Boolean(default= False)


class CrmXlsxReport(models.TransientModel):
    _name = 'crm.xlsx.report'
    _description = 'Description'
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')




    def action_all_download(self):
        data = {

        'type':'overall'
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'crm.xlsx.report',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'CRM XLSX REPORT',
                     },
            'report_type': 'crm_xlsx_report'
        }

    def action_xlsx_from_to(self):
        data = {
        'date_from':self.date_from,
        'date_to':self.date_to,
        'type':'summary_based_on_date'
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'crm.xlsx.report',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'CRM XLSX REPORT',
                     },
            'report_type': 'crm_xlsx_report'
        }

    #ordering the stages in dictionary
    def append_stage_in_one(self,dict):
        if not (dict==[]):
            result = {}
            for rec in dict:
                result[rec['id']] = {'name':rec['username'] }
            for rec in dict:
                result[rec['id']][rec['stage_id']] = {'name':rec['stage_name'],'stages_count':rec['stages_count'],'sequence':rec['sequence']}
            return result
        else:
            return []
    # executive summary



    def daily_report_write_table_executive(self,dict,sheet,workbook,header,row=0,col=1):
        heading = workbook.add_format({
            'bold': 2,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size':'24',
            'font_color':'white',
            'fg_color': '#6fa8dc'})
        header_of_table = workbook.add_format({
            'bold': 2,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size':'16',
            'font_color':'white',
            'fg_color': '#6fa8dc'})
        agent_style = workbook.add_format({
            'bold': 2,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '12',
            'font_color': 'black',
            'fg_color': '#efefef'})
        if dict == []:
            return row
        else:
            sheet.merge_range(row-1,0, row , col +7, header,heading)
            row = row+3
            first_row=row
            last_sequence =0
            row_col_name=[]
            row_col_vals=[]
            row_charts = row
            pie_chart_stages = []
            row = row + 20
            pie_chart_stages ={}
            self.env.cr.execute('''select name ,sequence from crm_stage ''')
            stages_order = self.env.cr.dictfetchall()
            count_of_stage =0
            for rec in  stages_order:
                # sheet.merge_range(row,col+rec['sequence'],row,col+rec['sequence']+1, rec['name'], heading)
                sheet.write(row,col+rec['sequence'],rec['name'],header_of_table)
                last_sequence = col+rec['sequence']
                pie_chart_stages[col+rec['sequence']]= {'start': row+1}
                sheet.set_column(0,col+rec['sequence']+1,20)
                count_of_stage = count_of_stage+1

            sheet.write(row, col +last_sequence,'Total',header_of_table)
            row = row + 1
            for row_name in range(row,len(dict.keys())+row):
                for col_name in range(0,count_of_stage+2):
                    sheet.write(row_name,col_name, '', agent_style)

                    # row_empty = row_empty + 1
            for rec in  dict.keys():
                total =0
                for data in dict[rec].keys():
                    if data =='name':
                        row_col_name.append([row,0])
                        sheet.write(row,0,dict[rec][data],agent_style)
                    else:
                        sheet.write(row,col+dict[rec][data]['sequence'],dict[rec][data]['stages_count'],agent_style)
                        total = total+ dict[rec][data]['stages_count']
                row_col_vals.append([row,col + last_sequence])
                sheet.write(row, col + last_sequence, total,agent_style)

                row = row+1
            for rec in  stages_order:
                last_sequence = col+rec['sequence']
                pie_chart_stages[col+rec['sequence']]['end']=  row+1


            chart1 = workbook.add_chart({'type': 'pie'})


            chart1.add_series({

                'data_labels': {'percentage': True},

                'categories': [ sheet.name,row_col_name[0][0], row_col_name[0][1], row_col_name[-1][0],row_col_name[-1][1]],
                'values': [ sheet.name,row_col_vals[0][0], row_col_vals[0][1], row_col_vals[-1][0],row_col_vals[-1][1]]
            })

            chart1.set_style(10)


            sheet.insert_chart(row_charts+3,0, chart1)

            print("yes i am tony")
            print("tab",sheet.name)
            print(pie_chart_stages)
            # barcharts o
            data_barcode =[]
            count =0
            chart2 = workbook.add_chart({'type': 'column'})
            for rec in pie_chart_stages.keys():
                temp = [{'name': ['Admin', 78, 1, 78, 1], 'categories': ['Admin', 78, 0, 78, 0], 'values': ['Admin', 78, 5, 78, 5]}, {'name': ['Admin', 78, 2, 78, 2], 'categories': ['Admin', 78, 0, 78, 0], 'values': ['Admin', 78, 5, 78, 5]}, {'name': ['Admin', 78, 3, 78, 3], 'categories': ['Admin', 78, 0, 78, 0], 'values': ['Admin', 78, 5, 78, 5]}, {'name': ['Admin', 78, 4, 78, 4], 'categories': ['Admin', 78, 0, 78, 0], 'values': ['Admin', 78, 5, 78, 5]}]
                if temp in data_barcode:
                    pass
                else:
                    data_barcode.append(temp)
                    for col in pie_chart_stages.keys():
                        chart2.add_series({
                            'name':  [sheet.name, pie_chart_stages[rec]['start']-1, col , pie_chart_stages[rec]['start']-1,col],
                            'categories': [ sheet.name,row_col_name[0][0], 0, row_col_name[-1][0],0],
                            'values':[ sheet.name,row_col_vals[0][0], col, row_col_vals[-1][0],col],
                         })

                        sheet.insert_chart('E'+str( pie_chart_stages[rec]['start']-17), chart2)

            return row



    def daily_report_executive_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id   
        and  (lead_created_date = date_trunc('day', CURRENT_DATE  - INTERVAL '1 DAY' ))
         and (lead_created_date < date_trunc('day', CURRENT_DATE  )) 

         
        and res_users.is_executive = True 
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Daily Summary of Executive',row)
        return row

    def weekly_report_executive_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('week', CURRENT_DATE) 
        and res_users.is_executive = True 
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet,workbook, 'Weekly Summary of Executive',row)
        return row

    def monthly_report_executive_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('month', CURRENT_DATE) 
        and res_users.is_executive = True 
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet,workbook, 'Monthly Summary of Executive',row)
        return row

    def yearly_report_executive_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('year', CURRENT_DATE) 
        and res_users.is_executive = True 
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet,workbook,'Yearly Summary of Executive', row)
        return row

    # dealers summary

    def daily_report_dealers_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id 
        
                and  (lead_created_date = date_trunc('day', CURRENT_DATE  - INTERVAL '1 DAY' ))
         and (lead_created_date < date_trunc('day', CURRENT_DATE  )) 
         
        and (res_users.is_executive = False or res_users.is_executive is Null)
		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
		and res_partner.id != 3
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        print('daily_report_dealers_summary_table')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        print(json_formate)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Daily Summary of Dealers',row)
        return row

    def weekly_report_dealers_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
           select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('week', CURRENT_DATE) 
        and (res_users.is_executive = False or res_users.is_executive is Null)
		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
		and res_partner.id != 3
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
           ''')
        dictionary = self.env.cr.dictfetchall()
        print('weekly_report_dealers_summary_table')

        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet,workbook,'Weekly Summary of Dealers', row)
        return row

    def monthly_report_dealers_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('month', CURRENT_DATE) 
        and (res_users.is_executive = False or res_users.is_executive is Null)
		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
		and res_partner.id != 3
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
           ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Monthly Summary of Dealers',row)
        return row

    def year_report_dealers_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('year', CURRENT_DATE) 
        and (res_users.is_executive = False or res_users.is_executive is Null)
		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
		and res_partner.id != 3
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
           ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Yearly Summary of Dealers',row)
        return row

    # extractors contractors

    def daily_report_contractors_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
       select res_contractors.id,res_contractors.name as username ,crm_stage.name as stage_name,
       crm_stage.id  as stage_id ,count(res_contractors.id)  as stages_count ,crm_stage.sequence from       
        crm_lead,
        res_contractors,
        crm_stage

        where

        crm_lead.based_on_contract = True and
        crm_lead.stage_id = crm_stage.id and
        crm_lead.contractor_id = res_contractors.id 
        
        
                and  (crm_lead.lead_created_date = date_trunc('day', CURRENT_DATE  - INTERVAL '1 DAY' ))
         and (crm_lead.lead_created_date < date_trunc('day', CURRENT_DATE  )) and
        
        crm_lead.active = True 
        group by res_contractors.id,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Daily Summary of Contractor',row)
        return row

    def weekly_report_contractors_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
          select res_contractors.id,res_contractors.name as username ,crm_stage.name as stage_name,
          crm_stage.id  as stage_id ,count(res_contractors.id)  as stages_count ,crm_stage.sequence from       
           crm_lead,
           res_contractors,
           crm_stage
           where
           crm_lead.based_on_contract = True and
           crm_lead.stage_id = crm_stage.id and
           crm_lead.contractor_id = res_contractors.id and
           crm_lead.lead_created_date >= date_trunc('week', CURRENT_DATE)  and
           crm_lead.active = True 
           group by res_contractors.id,crm_stage.id
               ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Weekly Summary of Contractor',row)
        return row

    def month_report_contractors_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
             select res_contractors.id,res_contractors.name as username ,crm_stage.name as stage_name,
             crm_stage.id  as stage_id ,count(res_contractors.id)  as stages_count ,crm_stage.sequence from       
              crm_lead,
              res_contractors,
              crm_stage
              where
              crm_lead.based_on_contract = True and
              crm_lead.stage_id = crm_stage.id and
              crm_lead.contractor_id = res_contractors.id and
              crm_lead.lead_created_date >= date_trunc('month', CURRENT_DATE)  and
              crm_lead.active = True 
              group by res_contractors.id,crm_stage.id
                  ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Monthly Summary of Contractor',row)
        return row

    def year_report_contractors_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
                select res_contractors.id,res_contractors.name as username ,crm_stage.name as stage_name,
                crm_stage.id  as stage_id ,count(res_contractors.id)  as stages_count ,crm_stage.sequence from       
                 crm_lead,
                 res_contractors,
                 crm_stage
                 where
                 crm_lead.based_on_contract = True and
                 crm_lead.stage_id = crm_stage.id and
                 crm_lead.contractor_id = res_contractors.id and
                 crm_lead.lead_created_date >= date_trunc('year', CURRENT_DATE)  and
                 crm_lead.active = True 
                 group by res_contractors.id,crm_stage.id
                     ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Yearly Summary of Contractor',row)
        return row

    # Admin Summary

    def daily_report_admin_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
            from
            crm_lead,crm_stage,res_users,res_partner where
            crm_lead.user_id = res_users.id 
            and res_users.partner_id = res_partner.id
              
                and  (lead_created_date = date_trunc('day', CURRENT_DATE  - INTERVAL '1 DAY' ))
         and (lead_created_date < date_trunc('day', CURRENT_DATE  )) 
            
            
            and (res_users.is_executive = False or res_users.is_executive is Null)
    		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
            and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
    		and res_partner.id = 3
            group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Daily Summary of Admin',row)
        return row

    def weekly_report_admin_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
            from
            crm_lead,crm_stage,res_users,res_partner where
            crm_lead.user_id = res_users.id 
            and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('week', CURRENT_DATE) 
            and (res_users.is_executive = False or res_users.is_executive is Null)
    		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
            and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
    		and res_partner.id = 3
            group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Weekly Summary of Admin',row)
        return row

    def month_report_admin_summary_table(self, sheet,workbook, row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
            from
            crm_lead,crm_stage,res_users,res_partner where
            crm_lead.user_id = res_users.id 
            and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('month', CURRENT_DATE) 
            and (res_users.is_executive = False or res_users.is_executive is Null)
    		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
            and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
    		and res_partner.id = 3
            group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Monthly Summary of Admin',row)
        return row

    def yearly_report_admin_summary_table(self, sheet, workbook,row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
            from
            crm_lead,crm_stage,res_users,res_partner where
            crm_lead.user_id = res_users.id 
            and res_users.partner_id = res_partner.id and  lead_created_date >= date_trunc('year', CURRENT_DATE) 
            and (res_users.is_executive = False or res_users.is_executive is Null)
    		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
            and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
    		and res_partner.id = 3
            group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,'Yearly Summary of Admin',row)
        return row

    # date based result
    def from_report_executive_summary_table(self, sheet, workbook,date_from,date_to, row):
        print('''lead_created_date between '''+"'"+date_from+"' and '"+date_to+"' )")
        self.env.cr.execute('''
           select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
           from
           crm_lead,crm_stage,res_users,res_partner where
           crm_lead.user_id = res_users.id 
           and res_users.partner_id = res_partner.id   
           and  (lead_created_date between '''+"'"+date_from+"' and '"+date_to+"' )"+

           '''and res_users.is_executive = True 
           and crm_lead.stage_id = crm_stage.id and crm_lead.active = True
           group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
           ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook, 'Summary of Executive', row)
        return row
    def from_report_dealers_summary_table(self, sheet,workbook, date_from,date_to,row):
        self.env.cr.execute('''
        select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
        from
        crm_lead,crm_stage,res_users,res_partner where
        crm_lead.user_id = res_users.id 
        and res_users.partner_id = res_partner.id 
            and  (lead_created_date between '''+"'"+date_from+"' and '"+date_to+"' )"+'''
         
        and (res_users.is_executive = False or res_users.is_executive is Null)
		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
        and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
		and res_partner.id != 3
        group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
        ''')
        print('daily_report_dealers_summary_table')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        print(json_formate)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook,' Summary of Dealers',row)
        return row

    def from_report_contractors_summary_table(self, sheet, workbook,  date_from,date_to,row):
        self.env.cr.execute('''
       select res_contractors.id,res_contractors.name as username ,crm_stage.name as stage_name,
       crm_stage.id  as stage_id ,count(res_contractors.id)  as stages_count ,crm_stage.sequence from       
        crm_lead,
        res_contractors,
        crm_stage

        where

        crm_lead.based_on_contract = True and
        crm_lead.stage_id = crm_stage.id and
        crm_lead.contractor_id = res_contractors.id 

            and  (lead_created_date between '''+"'"+date_from+"' and '"+date_to+"' )"+''' and


        crm_lead.active = True 
        group by res_contractors.id,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook, 'Summary of Contractor', row)
        return row

    def from_report_admin_summary_table(self, sheet, workbook, date_from,date_to,row):
        self.env.cr.execute('''
            select res_partner.id,res_partner.name as username,crm_stage.name as stage_name ,crm_stage.id as stage_id,count(res_partner.id) as stages_count ,crm_stage.sequence
            from
            crm_lead,crm_stage,res_users,res_partner where
            crm_lead.user_id = res_users.id 
            and res_users.partner_id = res_partner.id

            and  (lead_created_date between '''+"'"+date_from+"' and '"+date_to+"' )"+''' 


            and (res_users.is_executive = False or res_users.is_executive is Null)
    		and (crm_lead.based_on_contract = False or crm_lead.based_on_contract is Null)
            and crm_lead.stage_id = crm_stage.id and crm_lead.active = True 
    		and res_partner.id = 3
            group by res_partner.id,crm_stage.name ,crm_stage.sequence,crm_stage.id
            ''')
        dictionary = self.env.cr.dictfetchall()
        json_formate = self.append_stage_in_one(dictionary)
        row = self.daily_report_write_table_executive(json_formate, sheet, workbook, 'Summary of Admin', row)
        return row

    def write_pending_activities(self,workbook,sheet,row):
         print("worksheet",workbook)
         heading = workbook.add_format({
             'bold': 2,
             'border': 1,
             'align': 'center',
             'valign': 'vcenter',
             'font_size': '18',
             'font_color': 'white',
             'fg_color': '#6fa8dc'})

         heading_status = workbook.add_format({
             'bold': 2,
             'border': 1,
             'align': 'center',
             'valign': 'vcenter',
             'font_size': '12',
             'font_color': 'white',
             'fg_color': '#6fa8dc'})
         sheet.merge_range(row, 0, row+1, 2, 'Pending Activity ', heading)
         row = row+1
         row = row+1

         activity =self.env['mail.activity'].sudo().search([(1,'=',1)])
         sheet.write(row, 0, 'Name',heading_status)
         sheet.write(row, 1, 'Due Date',heading_status)
         sheet.write(row, 2, 'Assigned',heading_status)
         row = row+1
         agent_style = workbook.add_format({
             'bold': 2,
             'border': 1,
             'align': 'center',
             'valign': 'vcenter',
             'font_size': '12',
             'font_color': 'black',
             'fg_color': '#efefef'})
         for rec in activity:
            sheet.write(row,0,rec.res_name,agent_style)
            sheet.write(row,1,str(rec.date_deadline),agent_style)
            sheet.write(row,2,str(rec.user_id.partner_id.name),agent_style)

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        if (data['type'] == 'overall'):
            sheet = workbook.add_worksheet('Executive')
            row = self.daily_report_executive_summary_table(sheet,workbook, 1)
            row = self.weekly_report_executive_summary_table(sheet,workbook, row + 4)
            row = self.monthly_report_executive_summary_table(sheet,workbook, row + 4)
            row = self.yearly_report_executive_summary_table(sheet,workbook, row + 4)
            self.write_pending_activities(workbook, sheet, row + 2)

            sheet2 = workbook.add_worksheet('Dealers')
            row = self.daily_report_dealers_summary_table(sheet2,workbook, 1)
            row = self.weekly_report_dealers_summary_table(sheet2,workbook, row + 4)
            row = self.monthly_report_dealers_summary_table(sheet2,workbook, row + 4)
            row = self.year_report_dealers_summary_table(sheet2,workbook, row + 4)
            self.write_pending_activities(workbook, sheet2, row + 2)

            #
            sheet3 = workbook.add_worksheet('Contractors')
            row = self.daily_report_contractors_summary_table(sheet3, workbook,1)
            row = self.weekly_report_contractors_summary_table(sheet3, workbook,row + 4)
            row = self.month_report_contractors_summary_table(sheet3,workbook, row + 4)
            row = self.year_report_contractors_summary_table(sheet3,workbook, row + 4)
            self.write_pending_activities(workbook, sheet3, row + 2)

            sheet4 = workbook.add_worksheet("Admin")
            row = self.daily_report_admin_summary_table(sheet4, workbook,1)
            row = self.weekly_report_admin_summary_table(sheet4, workbook,row + 4)
            row = self.month_report_admin_summary_table(sheet4, workbook,row + 4)
            row = self.yearly_report_admin_summary_table(sheet4, workbook,row + 4)
            self.write_pending_activities(workbook, sheet4, row + 2)

        else:
        #
            if data['date_from'] and data['date_to']:
                sheet = workbook.add_worksheet('Executive')
                print("yes")
                print(data)
                row = self.from_report_executive_summary_table(sheet, workbook, data['date_from'],data['date_to'],1)
                row = self.from_report_dealers_summary_table(sheet, workbook, data['date_from'],data['date_to'],row+3)
                row = self.from_report_contractors_summary_table(sheet, workbook, data['date_from'],data['date_to'],row+3)
                row = self.from_report_admin_summary_table(sheet, workbook, data['date_from'],data['date_to'],row+3)
                self.write_pending_activities(workbook,sheet,row+3)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()