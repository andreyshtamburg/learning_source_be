from http import HTTPStatus

from flask import Blueprint
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from app.exceptions import FieldValidationException

v1_blueprint = Blueprint('v1_blueprint', __name__)
v1_api = Api(
    v1_blueprint,
    title='Learning source api',
    version='1.0', description='Learning source api',
    # FIXME Unable to run tests if loading doc dynamically. Figure out why
    # doc=cfg['SWAGGER_DOC_PATH']
    doc='/doc/'
)

from .main.controller.SourceController import ls_ns


@v1_api.errorhandler(FieldValidationException)
def handle_validation_exception(error):
    exception_response = dict()
    exception_response['message'] = 'Validation error'
    exception_response['errors'] = error.exception_map if error.exception_map else {
        error.error_field_name: error.message}
    return exception_response, HTTPStatus.BAD_REQUEST


@v1_api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    """Return a custom not found error message and 404 status code"""
    return {'message': error.specific}, 404


v1_api.add_namespace(ls_ns)
