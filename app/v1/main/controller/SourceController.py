from http import HTTPStatus

from flask_restplus import Resource, Namespace, abort

from app.exceptions import FieldValidationException
from ..model.LearningSourceModel import *
from ..service.SourceService import SourceService
from ..service.TagService import TagService

ls_ns = Namespace('ls')


@ls_ns.route('/sources/<int:source_id>')
class LearningSource(Resource):
    source_service = SourceService()

    @ls_ns.marshal_with(Source.get_source_by_id_response_model,
                        code=HTTPStatus.OK,
                        description='Get source by id')
    def get(self, source_id):
        source = self.source_service.get_source_by_id(source_id)
        if source:
            return source, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, f'source with id `{source_id}` is not found')

    @ls_ns.marshal_with(Source.delete_source_response_model,
                        code=HTTPStatus.OK,
                        description='Delete source',
                        skip_none=True)
    def delete(self, source_id):
        source = self.source_service.delete_source(source_id)
        if source:
            return source, HTTPStatus.OK
        else:
            # TODO return the same looking response. Make delete idempotent.
            return f'{source_id}', HTTPStatus.OK

    @ls_ns.doc(body=Source.create_source_request_resource_model, validate=True)
    @ls_ns.marshal_with(Source.update_source_response_model,
                        code=HTTPStatus.OK,
                        description='Update source')
    def put(self, source_id):
        updated_source, exceptions = self.source_service.update_source(source_id, v1_api.payload)
        if exceptions:
            raise FieldValidationException(exception_map=exceptions)
        else:
            return updated_source, HTTPStatus.OK


@ls_ns.route('/')
class LearningSourceList(Resource):
    source_service = SourceService()

    @ls_ns.marshal_with(Source.get_sources_response_resource_model,
                        code=HTTPStatus.OK,
                        as_list=True,
                        description='Get all sources',
                        envelope='sources')
    def get(self):
        sources = self.source_service.get_all_sources()
        return sources, HTTPStatus.OK

    @ls_ns.doc(body=Source.create_source_request_resource_model, validate=True)
    @ls_ns.marshal_with(Source.create_source_response_resource_model,
                        code=HTTPStatus.CREATED,
                        description='Create new source')
    def post(self):
        data = v1_api.payload
        new_source, exceptions = self.source_service.save_new_source(data)
        if exceptions:
            raise FieldValidationException(exception_map=exceptions)
        else:
            return new_source, HTTPStatus.CREATED


@ls_ns.route('/tags')
class LearningSourceTagList(Resource):
    tag_service = TagService()

    @ls_ns.marshal_with(Tag.tag_response_resource_model,
                        code=HTTPStatus.OK,
                        as_list=True,
                        description='Get all tags',
                        envelope='tags')
    def get(self):
        tags = self.tag_service.get_all_tags()
        return tags, HTTPStatus.OK

