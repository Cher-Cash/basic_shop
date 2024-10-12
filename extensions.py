"""[summary]."""
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
admin_ext = Admin(template_mode='bootstrap3')
migrate_ext = Migrate()