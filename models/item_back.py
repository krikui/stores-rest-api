import sqlite3

class ItemModel(object):
    def __init__(self, name, price):
        self._name = name
        self._price = price
    
    def json(self):
        return {'name': self._name, 'price': self._price}
    
    @classmethod
    def find_by_itemName(cls, name):    #classmethod cause it returns clas item object and not dict
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))  # parameter should be tupple
        row = result.fetchone()
        connection.close()
    
        if row:
            # return {'item': {'name':row[0], 'price':row[1]}}
            return cls(*row)   #instead row[0], row[1]

    def update(self):
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            query = "UPDATE items SET price = ? WHERE name = ?"
            cursor.execute(query, (self._price, self._name))
        # return {"message": "Item {} price is updated to {}".format(self._name, self._price)}, 200


    def insert(self):
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            query = "INSERT INTO items VALUES(?, ?)"
            cursor.execute(query, (self._name, self._price),)