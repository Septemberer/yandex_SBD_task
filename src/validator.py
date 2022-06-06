from re import match as re_match
from models import ShopUnitType, ShopUnit, ShopUnitImport, ShopUnitImportRequest, ShopUnitStatisticUnit, ShopUnitStatisticResponse, Error
from exceptions import ValidationException
from datetime import datetime


def validate_long_time(element):
    if type(element) != str:
        raise ValidationException(
            'Переданный аргумент имеет неверный тип, ожидается строка')

    t = None
    try:
        t = datetime.strptime(element, '%Y-%m-%dT%H:%M:%S.%fZ')
    except Exception:
        raise ValidationException(
            'Cтрока имеет некорректный формат, пример формата: '
            '2021-01-10T09:32:14.42Z')
    return t



def validate_id(element):
    if type(element) == str:
        return element
    else:
        raise ValidationException(
            "Переданный аргумент имеет неверный тип, ожидается строка")

def validate_name(element):
    if type(element) == str:
        return element
    else:
        raise ValidationException(
            "Переданный аргумент имеет неверный тип, ожидается строка")


def validate_type(element):
    if element == 'CATEGORY':
        return ShopUnitType.category
    elif element == 'OFFER':
        return ShopUnitType.offer
    else:
        raise ValidationException(
            "Переданный аргумент должен иметь одно из "
            "значений перечисления ShopUnitType")

def validate_price(element):
    if type(element) == int:
        if element > 0:
            return element
        else:
            raise ValidationException(
                "Переданный аргумент должен быть положительным числом (> 0)")
    else:
        raise ValidationException(
            "Переданный аргумент имеет неверный тип, ожидается целое число")



def validate_ShopUnitImport(shop_unit_dict):
    try:
        id = validate_id(shop_unit_dict.get('id'))
    except Exception as e:
        raise ValidationException('Поле id - ' + str(e))

    try:
        name = validate_name(shop_unit_dict.get('name'))
    except Exception as e:
        raise ValidationException('Поле name - ' + str(e))
    
    try:
        parentId = validate_id(shop_unit_dict.get('parentId'))
    except Exception as e:
        raise ValidationException('Поле parentId - ' + str(e))

    try:
        type = validate_type(shop_unit_dict.get('type'))
    except Exception as e:
        raise ValidationException('type - ' + str(e))

    try:
        price = validate_price(shop_unit_dict.get('price'))
    except Exception as e:
        raise ValidationException('Поле price - ' + str(e))

    return ShopUnit(id, name, date, parentId, type, price, children)
