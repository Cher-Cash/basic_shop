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

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()