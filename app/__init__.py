from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager


db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__, template_folder='app/views')
    # Load configurations from config.py
    app.config.from_object(f"app.config.{config_name}")
    # Initialize extensions with app
    db.init_app(app)

    # login_manager = LoginManager(app)
    # login_manager.login_view = 'login'

    return app