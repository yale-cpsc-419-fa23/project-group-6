from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
    app.config['SECRET_KEY'] = '519'

    # Load configurations from config.py
    app.config.from_object(f"app.config.{config_name}")
    db.init_app(app)

    # Registering blueprints
    from app.controllers import auth_controller
    app.register_blueprint(auth_controller.auth)

    from app.controllers import main_controller
    app.register_blueprint(main_controller.main)

    from app.controllers import music_controller
    app.register_blueprint(music_controller.music)

    return app