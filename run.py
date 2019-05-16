from app6 import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    # db.delete()
    db.create_all()