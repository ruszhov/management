# import os
# from django.conf import settings
# import datetime
# import openpyxl
# import re
# import logging
# import subprocess
# import shlex
# from django.http import StreamingHttpResponse
#
# import sys
# import os.path
# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
#
# from parsing.models import *
# from parsing.parsers.functions import *
#
# def nasha_sprave(filename, contractor):
#     # exception = kw.pop('exception', Exception)
#     check_status = File.objects.get(file__icontains=filename, uploaded_at__date=datetime.date.today())
#
#     if check_status.status == 1:
#         try:
#             filepath = os.path.join(settings.MEDIA_ROOT, 'workflow', str(datetime.date.today()), filename)
#             wb = openpyxl.load_workbook(filepath)
#             sheet = wb.active
#             # get max row count
#             max_row = sheet.max_row
#             # get max column count
#             max_column = sheet.max_column
#             # iterate over all cells
#             # iterate over all rows
#
#             operator_id = operator_create('Наша справа', contractor)
#             year_id = year_create()
#             m = months_create()
#             free_status_id = free_status_create()
#
#             header_dictionary = {}
#             months_data = {}
#
#             def add_to_dict(k, v):
#                 try:
#                     months_data[k].append(v)
#                 except KeyError:
#                     months_data[k] = [v]
#
#             # get header row by number of string
#             headers = sheet[8]
#             for i in headers:
#                 header_dictionary[i.col_idx] = i.value
#
#             adr_list = ['Адреса щита', 'Адреса', 'Адреса сітілайта', 'адреси беклайтів']
#
#             # iterate trough headers keys and find col indexes
#             for k, v in header_dictionary.items():
#                 if 'url' in v:
#                     url_col = k
#                 elif 'Код' == v:
#                     kod_col = k
#                 elif 'Код Дорс' in v:
#                     doors_col = k
#                 elif (for a in adr_list) in v:
#                     address_col = k
#                 elif (for s in ['сторона', 'Сторона']) in v:
#                     side_col = k
#                 elif 'Освітлення' in v:
#                     light_col = k
#
#
#                 elif 'Область' in v:
#                     region_col = k
#                 elif 'Город' in v:
#                     city_col = k
#                 elif 'Район' in v:
#                     city_area_col = k
#                 elif 'Адреса щита' in v:
#                     address_col = k
#                 elif 'Формат' in v:
#                     type_col = k
#
#
#                 elif 'OTS' in v:
#                     ots_col = k
#                 elif 'GRP' in v:
#                     grp_col = k
#
#                 elif 'Цена грн. без НДС' in v:
#                     price_col = k
#                 elif 'Янв' in v:
#                     add_to_dict(1, k)
#                 elif 'Фев' in v:
#                     add_to_dict(2, k)
#                 elif 'Мар' in v:
#                     add_to_dict(3, k)
#                 elif 'Апр' in v:
#                     add_to_dict(4, k)
#                 elif 'Май' in v:
#                     add_to_dict(5, k)
#                 elif 'Июн' in v:
#                     add_to_dict(6, k)
#                 elif 'Июл' in v:
#                     add_to_dict(7, k)
#                 elif 'Авг' in v:
#                     add_to_dict(8, k)
#                 elif 'Сен' in v:
#                     add_to_dict(9, k)
#                 elif 'Окт' in v:
#                     add_to_dict(10, k)
#                 elif 'Ноя' in v:
#                     add_to_dict(11, k)
#                 elif 'Дек' in v:
#                     add_to_dict(12, k)
#                 else:
#                     pass
#             print(header_dictionary)
#             # iterating trough rows
#             for i in range(3, max_row + 1):
#                 current_row = i
#                 region_tmp = None
#                 city_tmp = None
#                 city_area_tmp = None
#                 media_type_tmp = None
#                 size_tmp = None
#                 side_tmp = None
#
#                 kod = sheet.cell(row=i, column=kod_col).value
#                 if kod is not None:
#
#                     region = sheet.cell(row=i, column=region_col).value
#                     if region and region != region_tmp:
#                         region_id = region_create(region)
#                         region_tmp = region
#
#                     city = sheet.cell(row=i, column=city_col).value
#                     if city and  city != city_tmp:
#                         city_id = city_create(city)
#                         city_tmp = city
#
#                     city_area = sheet.cell(row=i, column=city_area_col).value
#                     if city_area and city_area != city_area_tmp:
#                         city_area_id = city_area_create(city_area)
#                         city_area_tmp = city_area
#
#                     media_type_raw = sheet.cell(row=i, column=type_col).value
#                     str_split = media_type_raw.split()
#                     media_type = ''
#                     for l in str_split:
#                         if l.isalpha():
#                             media_type += l + ' '
#                         else:
#                             if '[' not in l:
#                                 size = l
#                             else:
#                                 pass
#
#                     if size != size_tmp:
#                         size_id = board_size_create(size)
#                         size_tmp = size
#
#                     if media_type != '' and media_type != media_type_tmp:
#                         media_type_id = media_type_create(media_type)
#                         media_type_tmp = media_type
#
#                     light = sheet.cell(row=i, column=light_col).value
#                     side = sheet.cell(row=i, column=side_col).value
#                     if side != side_tmp:
#                         board_side_id = board_side_create(side)
#                         side_tmp = side
#                     address = sheet.cell(row=i, column=address_col).value
#                     # kod = sheet.cell(row=i, column=kod_col).value
#                     price = sheet.cell(row=i, column=price_col).value
#                     if price:
#                         price_val = float(price)
#                     hyperlink = sheet.cell(row=i, column=url_col).hyperlink
#                     if hyperlink:
#                         url = hyperlink.target
#                     ots = sheet.cell(row=i, column=ots_col).value
#                     if ots:
#                         ots = int(ots)
#                     raw_grp = sheet.cell(row=i, column=grp_col).value
#                     if raw_grp and raw_grp != '':
#                         grp = float(raw_grp.replace(',', '.'))
#
#                     kod_doors = sheet.cell(row=i, column=doors_col).value
#                     if kod_doors:
#                         kod_doors_int = int(kod_doors)
#
#                     board_update = {
#                         'kod': kod,
#                         'url': url,
#                         'region_id': region_id if region_id else None,
#                         'city_id': city_id if city_id else None,
#                         'city_area_id': city_area_id if city_area_id else None,
#                         'address': address if address else None,
#                         'media_type_id': media_type_id if media_type_id else None,
#                         'size_id': size_id if size_id else None,
#                         'side_id': board_side_id if board_side_id else None,
#                         'light': True if light == 'Есть' else False,
#                         'ots': ots if ots else None,
#                         'grp': grp if grp else None,
#                         'kod_doors': kod_doors_int if kod_doors_int else None,
#                         'operator_id': operator_id
#                     }
#                     try:
#                         board = Board.objects.get(kod=kod, operator_id=operator_id)
#                         for key, value in board_update.items():
#                             setattr(board, key, value)
#                         board.save()
#                         display_format = "\nBoard, {}, has been edited."
#                         print(display_format.format(board))
#                     except Board.DoesNotExist:
#                         board_create = {
#                             'kod': kod,
#                             'url': url,
#                             'region_id': region_id if region_id else None,
#                             'city_id': city_id if city_id else None,
#                             'city_area_id': city_area_id if city_area_id else None,
#                             'address': address if address else None,
#                             'media_type_id': media_type_id if media_type_id else None,
#                             'size_id': size_id if size_id else None,
#                             'side_id': board_side_id if board_side_id else None,
#                             'light': True if light == 'Есть' else False,
#                             'ots': ots if ots else None,
#                             'grp': grp if grp else None,
#                             'kod_doors': kod_doors_int if kod_doors_int else None,
#                             'operator_id': operator_id
#                         }
#                         board_create.update(board_update)
#                         board = Board(**board_create)
#                         board.save()
#                         display_format = "\nBoard, {}, has been created."
#                         # print(display_format.format(board))
#
#                         #################################################################################################
#
#                     board_id = board.id
#
#                     for k, v in months_data.items():
#                         status = sheet.cell(row=i, column=v[0]).value
#                         if status != '' and status is not None:
#                             status_val = status.split(' ', 1)[0]
#                             # comparing statuses in file and in DB
#                             # if status_val == 'вільно':
#                             #     status_id = free_status_create()
#                             if status_val == 'Занято':
#                                 status_id = busy_status_create()
#                             elif status_val == 'Резерв':
#                                 status_id = rezerved_status_create()
#                             else:
#                                 st, created = Status.objects.get_or_create(
#                                     name=status_val,
#                                 )
#                                 status_id = st.id
#                         else:
#                             status_id = free_status_id
#
#                         status_price_update = {
#                             'status_id': status_id,
#                             'price': price_val,
#                             # 'month_id': k,
#                             # 'year_id': 1
#                         }
#                         try:
#                             price = StatusPrice.objects.get(board_id=board_id, year_id=year_id, month_id=k)
#                             for key, value in status_price_update.items():
#                                 setattr(price, key, value)
#                             price.save()
#                             display_format = "\nPrice, {}, has been edited."
#                             # print(display_format.format(price))
#                         except StatusPrice.DoesNotExist:
#                             status_price_create = {
#                                 'board_id': board_id,
#                                 'status_id': status_id,
#                                 'price': price_val,
#                                 'month_id': k,
#                                 'year_id': year_id
#                             }
#                             status_price_create.update(status_price_update)
#                             price = StatusPrice(**status_price_create)
#                             price.save()
#                             display_format = "\nPrice, {}, has been created."
#                             # print(display_format.format(price))
#
#             done_parsing(check_status.id)
#             return ({'octagon': 'parsed'})
#
#         except Exception as e:
#             error_parsing(check_status.id)
#             log_event(e, filename, contractor, current_row)
#             return ({'octagon': 'error', 'id': check_status.id})
#     else:
#         return ({'octagon': 'Data is parsed today'})