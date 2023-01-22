from flask_cors import CORS
from app.helpers import JSONEncoder
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import db as root_db, login_manager, ma
from .api.routes import api
from flask import Flask
from config import Config
from .authentication.routes import auth


app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app, root_db)

login_manager.init_app(app)
# Specify why page to load for Non-Authenticated users
login_manager.login_view = 'signin'

ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)
