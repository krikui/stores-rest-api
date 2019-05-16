#import sqlite3
from db import db


class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')   #property store now sees we have store_id thus allows to find store by id



    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name': self.name, 'price': self.price,'store_id': self.store_id}
    
    @classmethod
    def find_by_itemName(cls, name):    #classmethod cause it returns clas item object and not dict
        return cls.query.filter_by(name=name).first()   #select * from items where name=name
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name,))  # parameter should be tupple
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # return {'item': {'name':row[0], 'price':row[1]}}
        #     return cls(*row)   #instead row[0], row[1]

    # def update(self):
    #     with sqlite3.connect('data.db') as conn:
    #         cursor = conn.cursor()
    #         query = "UPDATE items SET price = ? WHERE name = ?"
    #         cursor.execute(query, (self._price, self._name))
    #     # return {"message": "Item {} price is updated to {}".format(self._name, self._price)}, 200


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # with sqlite3.connect('data.db') as conn:
        #     cursor = conn.cursor()
        #     query = "INSERT INTO items VALUES(?, ?)"
        #     cursor.execute(query, (self._name, self._price),)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
