from flask_restplus import Resource, Namespace
from http import HTTPStatus

from app.v1.main.model.learning_source import Source
from global_utils import get_global_parser


ls_ns = Namespace('ls')
parser = get_global_parser(ls_ns)


@ls_ns.route("/")
class LearningSource(Resource):
    @ls_ns.doc(validate=True)
    def get(self):
        sources = Source.query.all()
        if not sources:
            return '{"error": "No sources found"}', HTTPStatus.OK
