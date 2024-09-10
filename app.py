from datetime import datetime
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


migrate = Migrate()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate.init_app(app=app, db=db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    photo = db.Column(db.String(50))
    product = db.Column(db.String(50))
    description = db.Column(db.String(2048))
    discount = db.Column(db.Integer)
    attributes = db.relationship('Attributes', backref='product', lazy=True)
    orders = db.relationship('Orders', backref='product', lazy=True)


class Attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    value = db.Column(db.String(30))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(50))
    status = db.Column(db.String(10))
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()