from http import HTTPStatus

from flask_restplus import Resource, Namespace

from ..model.learning_source import Source

ls_ns = Namespace('ls')


@ls_ns.route("/")
class LearningSource(Resource):
    @ls_ns.doc()
    @ls_ns.marshal_with(Source.get_sources_response_resource_model,
                        code=HTTPStatus.OK,
                        as_list=True,
                        description='Get all users')
    def get(self):
        sources = Source.query.all()
        if sources:
            return sources, HTTPStatus.OK
        else:
            return "Nothing found", HTTPStatus.NOT_FOUND
