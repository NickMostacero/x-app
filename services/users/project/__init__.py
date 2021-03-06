# services/users/project/__init__.py


import os  # nuevo

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # nuevo
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS  # nuevo
from flask_migrate import Migrate  # nuevo
from flask_bcrypt import Bcrypt  # nuevo

# instanciamos la db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()  # nuevo
migrate = Migrate()
bcrypt = Bcrypt()


# nuevo
def create_app(script_info=None):
    # instanciado la app
    app = Flask(__name__)

    # establecer configuraicon
    app_settings = os.getenv('APP_SETTINGS')   # Nuevo
    app.config.from_object(app_settings)       # Nuevo

    # configuramos la extension
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)  # nuevo
    migrate.init_app(app, db)  # nuevo
    bcrypt.init_app(app)  # nuevo

    # registramos blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
