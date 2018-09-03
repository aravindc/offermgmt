from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from faker import Faker
from app.providers import MyProvider

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

orows = db.session.query(models.Offer).count()
prows = db.session.query(models.Product).count()

if orows is None or prows is None:
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()

if orows == 0 or prows == 0:
    fake = Faker()
    fake.add_provider(MyProvider)
    for _ in range(10):
        models.Product.seed(fake)
        models.Offer.seed(fake)
