from flask import Flask
from flask_mongoalchemy import MongoAlchemy

# global object for SQLAlchemy
db = MongoAlchemy()
# global object for flask logging
logger = None
# global object for flask config
cfg = None


def create_app(config_type='development'):
    """
    create flask application
    :param config_type: one of the following (development, testing, production)
    :return flask app object
    :rtype Flask
    """
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_type])

    global cfg
    cfg = app.config

    db.init_app(app)

    from .v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app
