from flask import Flask, jsonify, abort, request
import dal
import services
from models import Courier, CourierType, Order, ShopUnitImportRequest
from exceptions import ValidationException
import json
from json import loads as parse_json, dumps as generate_json
import validator


app = Flask(__name__)


# 1 Import товаров и категорий
@app.route('/imports', strict_slashes=False, methods=['POST'])
def import_couriers():
    try:
        data = request.data
        d = parse_json(data)['data']
    except Exception:
        return bad_request_with_message_code(
            'По ТЗ такое невозможно, но не удалось спарсить json в теле '
            'запроса, возможно отстутствует поле data')


    if d.get('items') is None:
        return bad_request_with_message_code(
            'По ТЗ такое невозможно, но отвутствует '
            'поле items')
    items = d.get('items')

    if d.get('updateDate') is None:
        return bad_request_with_message_code(
            'По ТЗ такое невозможно, но отвутствует '
            'поле updateDate')

    try:
        update_date = validator.validate_date(d.get('updateDate'))
    except ValidationException:
        return bad_request_code()

    ids_for_updating = []

    for e in items:
        if e.get('id') is None:
            return bad_request_with_message_code(
                'По ТЗ такое невозможно, но у ShopUnitImport отвутствует '
                'поле id')
        if services.get_shopunit_by_id(e.get('id')) is None:
            services.add_shop_unit_before(e, update_date)
        else:
            ids_for_updating.append(e.get('id'))
            services.change_shop_unit_before(e, update_date)

    items_from_bd = services.get_all_shopunits()

    for item in items_from_bd:
        parent = services.get_shopunit_by_id(item.get("parentId"))
        parent["children"] = sorted(list(set(parent.get("children")).add(item.get("id"))))
        try:
            services.update_shopunit(parent)
        except Exception:
            return bad_request_with_message_code(
                'Произошла какая-то шибка в базе данных')

    return ok_code(generate_json(shop_unit_import_request.to_dict()))     
        

        
# 2 Удаление по индификатору 

@app.route(
    '/delete/<string:id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_shop_unit_by_id(id):

    try:
        shop_unit = services.get_shopunit_by_id(id)
    except Exception:
        return not_found_code()  # Если ShopUnit не существует -> 404

    children_id = shop_unit.get("children")

    for ch_id in children_id:
        delete_shop_unit_by_id(ch_id)

    parent = services.get_shopunit_by_id(shop_unit.get("parentId"))
    parent["children"] = sorted(parent.get("children").remove(id))

    try:
        services.update_shopunit(parent)
        services.delete_shopunit(id)
    except Exception:
        return bad_request_with_message_code(
            'Произошла какая-то шибка в базе данных')

    return ok_code()



# 3 Информация об элементе

@app.route(
    '/nodes/<string:id>',
    strict_slashes=False,
    methods=['GET'])
def info_shop_unit_by_id(id):

    try:
        shop_unit = services.get_shopunit_by_id(id)
    except Exception:
        return not_found_code()  # Если ShopUnit не существует -> 404

    return ok_code(generate_json(shop_unit.to_dict()))




def ok_code(data=''):
    return data, 200, {'Content-Type': 'application/json; charset=utf-8'}


def created_code(data=''):
    return data, 201, {'Content-Type': 'application/json; charset=utf-8'}


def bad_request_code(data=''):
    return data, 400, {'Content-Type': 'application/json; charset=utf-8'}


def bad_request_with_message_code(message):
    body = generate_json({'error_message': message})
    return body, 400, {'Content-Type': 'application/json; charset=utf-8'}


def not_found_code(data=''):
    return data, 404, {'Content-Type': 'application/json; charset=utf-8'}


# Встроенный возвращает HTML, да ещё и текст, нужно это убрать
@app.errorhandler(404)
def not_found(error):
    return '', 404, {'Content-Type': 'application/json; charset=utf-8'}


@app.errorhandler(400)
def not_found(error):
    return '', 400, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)