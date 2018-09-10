from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_folder='../static/dist',
            template_folder='../static')
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models
