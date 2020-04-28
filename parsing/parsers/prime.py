import os, datetime, openpyxl, re, json, sys, os.path
from django.conf import settings

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from parsing.models import *
from parsing.parsers.functions import *
from django.http.response import StreamingHttpResponse

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time

@shared_task(bind=True)
def prime(self, filename, contractor):
    # exception = kw.pop('exception', Exception)
    check_status = File.objects.get(file__icontains=filename, uploaded_at__date=datetime.date.today())
    operator_id = operator_create('Прайм', contractor)
    header_row = 4
    table_first_row = 5
    light_presence = 'Да'
    sold_presence = 'Бронь'
    rezerv_presence = ['Резерв', 'Резерв,', '']

    if check_status.status == 1:
        try:
            if filename.endswith('.xls'):
                dir = os.path.join(settings.MEDIA_ROOT, 'workflow', str(datetime.date.today()))
                output = subprocess.run(['parsing/parsers/convert.sh', dir, filename])
                filepath = os.path.join(dir, filename + 'x')
            else:
                filepath = os.path.join(settings.MEDIA_ROOT, 'workflow', str(datetime.date.today()), filename)

            wb = openpyxl.load_workbook(filepath)
            sheet = wb.active
            # get max row count
            max_row = sheet.max_row
            # get max column count
            max_column = sheet.max_column
            # iterate over all cells
            # iterate over all rows
            header_dictionary = {}

            headers = sheet[header_row]
            for i in headers:
                header_dictionary[i.col_idx] = i.value

            kwargs = {
                'kod_col': 'Код',
                'url_col': 'Фото',
                'region_col': 'Область',
                'city_col': 'Город',
                'city_area_col': 'Район города',
                'address_col': 'Адрес поверхности',
                'type_col': 'Тип',
                'size_col': 'Размер',
                'side_col': 'Сторона',
                'light_col': 'Свет',
                'ots_col': 'OTS',
                'grp_col': 'GRP',
                'doors_col': 'Код DOORS'
            }
            args = (['Январь', 'Прайс Январь'],
                    ['Февраль', 'Прайс Февраль'],
                    ['Март', 'Прайс Март'],
                    ['Апрель', 'Прайс Апрель'],
                    ['Май', 'Прайс Май'],
                    ['Июнь', 'Прайс Июнь'],
                    ['Июль', 'Прайс Июль'],
                    ['Август', 'Прайс Август'],
                    ['Сентябрь', 'Прайс Сентябрь'],
                    ['Октябрь', 'Прайс Октябрь'],
                    ['Ноябрь', 'Прайс Ноябрь'],
                    ['Декабрь', 'Прайс Декабрь'])

            col_idx = get_value_from_header_dict(header_dictionary, **kwargs)
            col_idx_by_month = get_month_value_from_header_dict(header_dictionary, *args)

            #iterating trough rows
            for i in range(table_first_row, max_row + 1):
                region_tmp, region_id_tmp = None, None
                city_tmp, city_id_tmp = None, None
                city_area_tmp, city_area_id_tmp = None, None
                media_type_tmp, media_type_id_tmp = None, None
                size_tmp, size_id_tmp = None, None
                side_tmp, side_id_tmp = None, None
                address_tmp = None

                raw_kod = sheet.cell(row=i, column=col_idx['kod_col'][0]).value
                regex = re.compile('[-@_!#$%^&*()<>?/\|}{~:]')
                numbers = sum(c.isdigit() for c in raw_kod)

                if numbers < 5 or regex.search(raw_kod) is not None:

                    # for j in range(1, max_column + 1):

                    kod = raw_kod

                    hyperlink = sheet.cell(row=i, column=col_idx['url_col'][0]).hyperlink
                    url = hyperlink.target if hyperlink != '' and hyperlink is not None else None

                    region = sheet.cell(row=i, column=col_idx['region_col'][0]).value
                    region_id = tmp_checking(region, region_tmp, region_id_tmp, region_create)
                    region_tmp = region
                    region_id_tmp = region_id
                    
                    city = sheet.cell(row=i, column=col_idx['city_col'][0]).value.strip()
                    city_id = tmp_checking(city, city_tmp, city_id_tmp, city_create)
                    city_tmp = city
                    city_id_tmp = city_id

                    city_area = sheet.cell(row=i, column=col_idx['city_area_col'][0]).value
                    city_area_id = tmp_checking(city_area, city_area_tmp, city_area_id_tmp, city_area_create)
                    city_area_tmp = city_area
                    city_area_id_tmp = city_area_id

                    address = sheet.cell(row=i, column=col_idx['address_col'][0]).value
                    if address != '' and address is not None and address != address_tmp:
                        address = address
                    elif address != '' and address is not None and address == address_tmp:
                        address = address_tmp
                    else:
                        address = None
                    address_tmp = address

                    media_type = sheet.cell(row=i, column=col_idx['type_col'][0]).value
                    media_type_id = tmp_checking(media_type, media_type_tmp, media_type_id_tmp, media_type_create)
                    media_type_tmp = media_type
                    media_type_id_tmp = media_type_id

                    size = sheet.cell(row=i, column=col_idx['size_col'][0]).value
                    s = size.replace(',', '.').split(' ')[0]
                    size_id = tmp_checking(s, size_tmp, size_id_tmp, board_size_create)
                    size_tmp = s
                    size_id_tmp = size_id

                    side = sheet.cell(row=i, column=col_idx['side_col'][0]).value
                    board_side_id = tmp_checking(side, side_tmp, side_id_tmp, board_side_create)
                    side_tmp = side
                    side_id_tmp = board_side_id

                    raw_light = sheet.cell(row=i, column=col_idx['light_col'][0]).value
                    light = True if raw_light == light_presence else False

                    ots = sheet.cell(row=i, column=col_idx['ots_col'][0]).value
                    ots = int(ots) if ots != '' and ots is not None else None

                    raw_grp = sheet.cell(row=i, column=col_idx['grp_col'][0]).value
                    grp = float(raw_grp.replace(',', '.')) if raw_grp != '' and raw_grp is not None else None

                    kod_doors = sheet.cell(row=i, column=col_idx['doors_col'][0]).value
                    kod_doors_int = int(kod_doors) if kod_doors != '' and kod_doors is not None else None

                    # save_board(kod, url, region_id, city_id, city_area_id, address, media_type_id, size_id, board_side_id, light, ots, grp, kod_doors, operator_id)
                    board_id = save_board(kod, url, region_id, city_id, city_area_id, address, media_type_id,
                                          size_id,
                                          board_side_id, light, ots, grp, kod_doors_int, operator_id)

                    for k, v in col_idx_by_month.items():
                        status = sheet.cell(row=i, column=col_idx_by_month[k][0]).value
                        status_id = save_status(status, sold_presence, rezerv_presence)
                        price_val = float(sheet.cell(row=i, column=col_idx_by_month[k][1]).value)
                        save_status_price(board_id, status_id, price_val, k)
                else:
                    pass

                yield done_percent(i, max_row)

            # done_parsing(check_status.id)
        except Exception as e:
            # error_parsing(check_status.id)
            log_event(e, filename, contractor, i)
            yield ({contractor: 'error'})
    else:
        pass

