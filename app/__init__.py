from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'app/uploads/'

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
    app.config['SECRET_KEY'] = '519'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    from app.controllers import settings_controller
    app.register_blueprint(settings_controller.settings)

    from app.controllers import user_controller
    app.register_blueprint(user_controller.user)

    return app
