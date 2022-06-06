import enum

class ShopUnitType(enum.Enum):
    offer = "OFFER"
    category = "CATEGORY"


class ShopUnit():
    def __init__(self, id, name, date, parentId, type, price, children):
        self.id = id
        self.name = name
        self.date = date
        self.parentId = parentId
        self.type = type
        self.price = price
        self.children = children
        self.children.sort()

    def to_dict(self):
        if self.type is None:
            tname = None
        else:
            tname = self.type.name

        return {
            "id": self.id,
            "name": self.name,
            "date" : self.date,
            "parentId": self.parentId,
            "type": tname,
            "price": self.price,
            "children": [str(e) for e in self.children]
        }
    def to_db_entity(self):
        return (
            self.id,
            self.name,
            self.date,
            self.parentId,
            self.type.value,
            self.price,
            [[e.id, e.name, e.date, e.parentId, e.type, e.price, e.children] for e in self.children]
        )

    def __str__(self):
        return "({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(
            self.id,
            self.name,
            self.date,
            self.parentId,
            self.type,
            self.price,
            self.children)

class ShopUnitImport():
    def __init__(self, id, name, parentId, type, price):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.type = type
        self.price = price

    def to_dict(self):
        if self.type is None:
            tname = None
        else:
            tname = self.type.name

        return {
            "id": self.id,
            "name": self.name,
            "parentId": self.parentId,
            "type": tname,
            "price": self.price
        }
    def to_db_entity(self):
        return (
            self.id,
            self.name,
            self.parentId,
            self.type.value,
            self.price
        )

    def __str__(self):
        return "({0}, {1}, {2}, {3}, {4})".format(
            self.id,
            self.name,
            self.parentId,
            self.type,
            self.price)


class ShopUnitImportRequest():
    def __init__(self, items, updateDate):
        self.items = items,
        self.updateDate = updateDate

    def to_dict(self):
        return {
            "items": self.items,
            "updateDate": self.updateDate,
        }

    def to_db_entity(self):
        return (
            self.items,
            self.updateDate
        )

    def __str__(self):
        return "({0}, {1})".format(
            self.items,
            self.updateDate)

class ShopUnitStatisticUnit():
    def __init__(self, id, name, date, parentId, type, price):
        self.id = id
        self.name = name
        self.date = date
        self.parentId = parentId
        self.type = type
        self.price = price

    def to_dict(self):
        if self.type is None:
            tname = None
        else:
            tname = self.type.name

        return {
            "id": self.id,
            "name": self.name,
            "date" : self.date,
            "parentId": self.parentId,
            "type": tname,
            "price": self.price
        }
    def to_db_entity(self):
        return (
            self.id,
            self.name,
            self.date,
            self.parentId,
            self.type.value,
            self.price
        )

    def __str__(self):
        return "({0}, {1}, {2}, {3}, {4}, {5})".format(
            self.id,
            self.name,
            self.date,
            self.parentId,
            self.type,
            self.price)

class ShopUnitStatisticResponse():
    def __init__(self, items):
        self.items = items
        self.items.sort()

    def to_dict(self):
        return {
            "items": [str(e) for e in self.items]
        }

    def to_db_entity(self):
        return (
            [[e.id, e.name, e.date, e.parentId, e.type, e.price] for e in self.children]
        )

    def __str__(self):
        return "({0})".format(
            self.items)

class Error():
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }
    
    def to_db_entity(self):
        return (
            self.code,
            self.message
        )

    def __str__(self):
        return "({0}, {1})".format(
            self.code,
            self.message)