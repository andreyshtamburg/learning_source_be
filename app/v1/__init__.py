from flask import Blueprint
from flask_restplus import Api

from app import cfg
from .main.controller.source_controller import ls_ns

v1_blueprint = Blueprint('v1_blueprint', __name__)
v1_api = Api(
    v1_blueprint,
    title='Learning source api',
    version='1.0', description='Learning source api',
    doc=cfg['SWAGGER_DOC_PATH']
)

v1_api.add_namespace(ls_ns)
