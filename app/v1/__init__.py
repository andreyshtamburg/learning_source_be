from flask import Blueprint
from flask_restplus import Api

from app import cfg

v1_blueprint = Blueprint('v1_blueprint', __name__)
v1_api = Api(
    v1_blueprint,
    title='Learning source api',
    version='1.0', description='Learning source api',
    # FIXME Unable to run tests if load doc dynamically. Figure out why
    # doc=cfg['SWAGGER_DOC_PATH']
    doc='/doc/'
)

from .main.controller.source_controller import ls_ns
v1_api.add_namespace(ls_ns)
