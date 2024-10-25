from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from extensions import db
from datetime import datetime


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    photo = Column(String(200))
    product = Column(String(50))
    description = Column(String(2048))
    price = Column(Integer)
    discount = Column(Integer)
    attributes = relationship('Attributes', backref='product', lazy=False)
    orders = relationship('Orders', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'


class Attributes(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    value = Column(String(30))
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class Orders(db.Model):
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.now)
    email = Column(String(50))
    status = Column(String(10))
    prod_id = Column(Integer, ForeignKey('product.id'), nullable=False)
