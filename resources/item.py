from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This "price" field cannot be empty')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This store_id cannot be empy')

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

            data = self.parser.parse_args()
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
            try:
                item.save_to_db()
            except:
                return {'message': 'Error while insert the item'}, 500
            return item.json(), 200

    def delete(self, name):
        item = ItemModel.find_by_itemName(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item {} deleted'.format(name)}, 200
        return {'message': 'Item {} not found'.format(name)}, 400



    def put(self, name):
        data = Item.parser.parse_args()
        # item = {'name': name, 'price': data['price']}
        item = ItemModel.find_by_itemName(name)

        if item:
            try:
                # self.update(item)
                # if (data['price'] == item.price and data['store_id'] == item.store_id):
                #     return {"message": "Price: {p}, Store_id {id} for item: {i} weren't changed".format(p=data['price'], i=name, id=data['store_id'])}, 400

                if (data['price'] != item.price and data['store_id'] == item.store_id) :
                    item.price = data['price']
                    item.save_to_db()

                elif (data['price'] == item.price and data['store_id'] != item.store_id):
                    item = ItemModel(name, **data)
                    item.save_to_db()
                else:
                    return {"message": "Price: {p}, Store_id {id} for item: {i} hasn't changed".format(p=data['price'], i=name, id=data['store_id'])}, 400
            except:
                return {"message": "Error happened in server while updating"}, 500
        else:
            try:
                item = ItemModel(name, **data)
                item.save_to_db()

            except:
                return {"message": "Error happened in server while inserting"}, 500

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

        return {'items': [item.json() for item in ItemModel.query.order_by(ItemModel.store_id.asc()).all()]}
        # return {'items': list(map(lambda x: x.json), ItemModel.query.all())}