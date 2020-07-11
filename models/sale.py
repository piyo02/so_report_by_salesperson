# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class SaleSalespersonReport(models.TransientModel):
    _name = 'sale.salesperson.report'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)
    user_ids = fields.Many2many('res.users', string="Salesperson")

    @api.multi
    def print_salesperson_vise_report(self):
        sale_orders = self.env['sale.order'].search([
            ('state', '=', 'sale'),
            ('invoice_status', '=', 'invoiced')
        ])
        groupby_dict = {}
        for user in self.user_ids:
            filtered_order = list(filter(lambda x: x.user_id == user, sale_orders))
            filtered_by_date = list(
                filter(lambda x: x.date_order >= self.start_date and x.date_order <= self.end_date, filtered_order))
            groupby_dict[user.name] = filtered_by_date

        final_dict = {}
        for user in groupby_dict.keys():
            temp = []
            for order in groupby_dict[user]:
                temp_2 = []
                temp_2.append(order.name)
                temp_2.append(order.date_order)
                temp_2.append(order.amount_total)
                temp_2.append(order.partner_id.display_name)
                temp.append(temp_2)
            final_dict[user] = temp
        datas = {
            'ids': self.ids,
            'model': 'sale.salesperson.report',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self,'sr_sales_report_saleperson_groupby.saleperson_temp', data=datas)
