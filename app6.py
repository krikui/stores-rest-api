from datetime import timedelta
import os

from resources.item import Item, ItemList

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from resources.user import UserRegister
from security import authenticate, identity
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  #choose env var DB from Heroku, if not use local sqlite


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kashya'
api = Api(app)

# @app.before_first_request   moved to run.py
# def create_tables():
#     # db.delete()
#     db.create_all()  #sqlAlchemy goes through imports above and gets to models and creates tables and columns

# If we want to change the url to the authentication endpoint, for instance, we want to
# use /login instead of /auth
# app.config(JWT_AUTH_URL_RULE) = '/login'

# config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(app, authenticate, identity)  #auth



api.add_resource(Item, '/item/<string:name>')  #http:127.0.0.1/student/Danny
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# api.add_resource(Users, '/users')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)