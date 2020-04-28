import datetime
import sys
import os.path
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from parsing.models import *

def year_create():
    year, created = Year.objects.get_or_create(
        name=datetime.datetime.now().year
    )
    return int(year.id)

def months_create():
    months = {1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень', 5: 'Травень', 6: 'Червень', 7: 'Липень',
              8: 'Серпень', 9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'}
    for k, v in months.items():
        month, created = Month.objects.get_or_create(
            id=k, name=v
        )
    return months

def operator_create(value, slug):
    operator, created = Operator.objects.get_or_create(
        name=value, slug=slug,
    )
    return int(operator.id)

def get_value_from_header_dict(dict, *args, **kwargs):
    result = {}
    for key, value in kwargs.items():
        for k, v in dict.items():
            if value == v:
                if key not in result.keys():
                    result[key] = [k]
                else:
                    result[key].append(k)
    return result

def get_month_value_from_header_dict(dict, *args):
    result = {}
    for i in args:
        for k, v in dict.items():
            if isinstance(i, list):
                for item in i:
                    if item in v:
                        if args.index(i) + 1 not in result.keys():
                            result[args.index(i) + 1] = [k]
                        else:
                            result[args.index(i) + 1].append(k)
            else:
                if i in v:
                    if args.index(i) + 1 not in result.keys():
                        result[args.index(i) + 1] = [k]
                    else:
                        result[args.index(i) + 1].append(k)
    return result


def free_status_create():
    free_status, created = Status.objects.get_or_create(
        name='Вільно',
    )
    return int(free_status.id)

def rezerved_status_create():
    rezerved_status, created = Status.objects.get_or_create(
        name='Зарезервовано',
    )
    return int(rezerved_status.id)

def busy_status_create():
    busy_status, created = Status.objects.get_or_create(
        name='Зайнято',
    )
    return int(busy_status.id)

def region_create(value):
    region, created = Region.objects.get_or_create(
        name=value.strip().capitalize(),
    )
    return str(region.id)

def city_create(value):
    city, created = City.objects.get_or_create(
        name=value.strip().capitalize(),
    )
    return str(city.id)

def city_area_create(value):
    city_area, created = CityArea.objects.get_or_create(
        name=value.strip().capitalize(),
    )
    return str(city_area.id)

def media_type_create(value):
    media_type, created = MediaType.objects.get_or_create(
        name=value.strip().capitalize(),
    )
    return str(media_type.id)

def board_side_create(value):
    board_side, created = Side.objects.get_or_create(
        name=value,
    )
    return str(board_side.id)

def board_size_create(value):
    board_size, created = BoardSize.objects.get_or_create(
        name=value,
    )
    return str(board_size.id)

def tmp_checking(value, value_tmp, id_tmp, create_function):
    if value != '' and value is not None and value != value_tmp:
        value_id = create_function(value)
        return value_id
    elif value == value_tmp:
        return id_tmp
    else:
        return None

def done_parsing(id):
    done = File.objects.get(id=id)
    setattr(done, 'status', 3)
    done.save()
    return str(done.id)

def error_parsing(id):
    done = File.objects.get(id=id)
    setattr(done, 'status', 5)
    done.save()
    return str(done.id)

def log_event(e, filename, contractor, row):
    extra = {'app_name': filename, 'row': row}
    logger = logging.getLogger(filename)
    if not logger.handlers:
        syslog = logging.FileHandler(os.path.join('parsing', 'logs', contractor + "." + 'log'), 'a+')
        formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s - row: %(row)s')
        syslog.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(syslog)
        logger = logging.LoggerAdapter(logger, extra)
        logger.info(e)

def save_board(kod, url, region_id, city_id, city_area_id, address, media_type_id, size_id, board_side_id, light, ots, grp, kod_doors, operator_id ):
    board_update = {
        'kod': kod,
        'url': url,
        'region_id': region_id,
        'city_id': city_id,
        'city_area_id': city_area_id,
        'address': address,
        'media_type_id': media_type_id,
        'size_id': size_id,
        'side_id': board_side_id,
        'light': light,
        'ots': ots,
        'grp': grp,
        'kod_doors': kod_doors,
        'operator_id': operator_id
    }

    try:
        board = Board.objects.get(kod=kod, side_id=board_side_id, operator_id=operator_id)
        for key, value in board_update.items():
            setattr(board, key, value)
        board.save()
        display_format = "Board, {}, has been edited."
        print(display_format.format(board))
    except Board.DoesNotExist:
        board_create = {
            'kod': kod,
            'url': url,
            'region_id': region_id,
            'city_id': city_id,
            'city_area_id': city_area_id,
            'address': address,
            'media_type_id': media_type_id,
            'size_id': size_id,
            'side_id': board_side_id,
            'light': light,
            'ots': ots,
            'grp': grp,
            'kod_doors': kod_doors,
            'operator_id': operator_id
        }
        board_create.update(board_update)
        board = Board(**board_create)
        board.save()
        display_format = "Board, {}, has been created."
        print(display_format.format(board))
    return str(board.id)

def save_status(status, st_bron, st_rezerv):
    if status != '' and status is not None:
        status_val = status.strip().replace(',', '')
        if status_val == st_bron:
            status_id = busy_status_create()
        elif isinstance(st_bron, list) and status_val in st_bron:
            status_id = busy_status_create()
        elif status_val == st_rezerv:
            status_id = rezerved_status_create()
        elif isinstance(st_rezerv, list) and status_val in st_rezerv:
            status_id = rezerved_status_create()
        else:
            st, created = Status.objects.get_or_create(
                name=status_val,
            )
            status_id = st.id
        return status_id
    else:
        status_id = free_status_create()
        return str(status_id)

def save_status_price(board_id, status_id, price_val, month_id):
    status_price_update = {
        'board_id': board_id,
        'status_id': status_id,
        'price': price_val,
        'month_id': month_id,
        'year_id': year_create()
    }
    try:
        price = StatusPrice.objects.get(board_id=board_id, month_id=month_id)
        for key, value in status_price_update.items():
            setattr(price, key, value)
        price.save()
        display_format = "\nPrice, {}, has been edited."
        # print(display_format.format(price))
    except StatusPrice.DoesNotExist:
        status_price_create = {
            'board_id': board_id,
            'status_id': status_id,
            'price': price_val,
            'month_id': month_id,
            'year_id': year_create()
        }
        status_price_create.update(status_price_update)
        price = StatusPrice(**status_price_create)
        price.save()
        display_format = "\nPrice, {}, has been created."
        # print(display_format.format(price))
    return str(price.id)

def done_percent(current_row, total_row):
    percentage = current_row / total_row * 100
    return int(percentage)