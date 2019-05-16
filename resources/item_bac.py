from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):

    @staticmethod
    def reqparsing(*args):
        parser = reqparse.RequestParser()
        parser.add_argument(
            str(args[0]),
            type=float,
            required=True,
            help='This {} field cannot be empty'.format(args[0])
        )
        return parser.parse_args()


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_itemName(name)
        if item:
            # return {'item': {'name': item['name'], 'price': item['price']}}, 200
            return item.json(), 200
        return {'message': "Item not found"}, 404

    def post(self, name):
        # if ItemModel.find_by_itemName(name):
        if ItemModel.find_by_itemName(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        else:
            data = Item.reqparsing("price")
            # item = {'name': name, 'price': data['price']}
            item = ItemModel(name, data['price'])
            try:
                # ItemModel.insert(item)
                # item.insert()
                item.save_to_db()
            except:
                return {'message': 'Error while insert the item'}, 500
            return item.json(), 200

    def delete(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)  # first occurance of item[name]
        # if not ItemModel.find_by_itemName(name):
        #     return {'message': "An item with name '{}' doesn't exist".format(name)}, 400
        # else:
        #     with sqlite3.connect('data.db') as conn:
        #         cursor = conn.cursor()
        #         query = "DELETE FROM items WHERE name = ?"
        #         cursor.execute(query, (name,))
        # return {'message': 'Item {} deleted'.format(name)}, 200
        item = ItemModel.find_by_itemName(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item {} deleted'.format(name)}, 200
        return {'message': 'Item {} not found'.format(name)}, 400



    def put(self, name):
        data = Item.reqparsing("price")
        # item = {'name': name, 'price': data['price']}
        item = ItemModel.find_by_itemName(name)

        if item:
            try:
                # self.update(item)
                if (data['price'] != item.price):
                    item.price = data['price']
                # item.save_to_db()
                else:
                    return {"message": "Price: {p} for item: {i} hasn't changed".format(p=data['price'], i=name)}, 400
            except:
                return {"message": "Error happened in server while updating"}, 500
        else:
            try:
                # item.insert()
                item = ItemModel(name, data['price'])

            except:
                return {"message": "Error happened in server while inserting"}, 500
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        # with sqlite3.connect('data.db') as conn:
        #     cursor = conn.cursor()
        #     query = "SELECT * from items"
        #     res = cursor.execute(query)
        #     rows = res.fetchall()
        #     Items = []
        #     for row in rows:
        #         Items.append({"id": row[0], "name": row[1], 'price': row[2]})
        #     return {"items": Items}

        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json), ItemModel.query.all())}