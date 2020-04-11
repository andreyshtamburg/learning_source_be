from http import HTTPStatus

from flask_restplus import Resource, Namespace, abort

from app.exceptions import FieldValidationException
from ..model.LearningSourceModel import *
from ..service.SourceService import SourceService

ls_ns = Namespace('ls')


@ls_ns.route('/sources/<int:source_id>')
class LearningSource(Resource):
    source_service = SourceService()

    @staticmethod
    def find_one(source_id):
        return Source.query.filter_by(id=source_id).first()

    @staticmethod
    def find_tags(payload):
        request_tags = [x.lower() for x in [tag['name'] for tag in payload['tags']]]
        found_tags = [Tag.query.filter_by(name=tag).first() for tag in request_tags]
        return found_tags

    @ls_ns.marshal_with(Source.get_source_by_id_response_model,
                        code=HTTPStatus.OK,
                        description='Get source by id')
    def get(self, source_id):
        match = self.find_one(source_id)
        if match is not None:
            return match, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, f'source with id `{source_id}` is not found')

    @ls_ns.marshal_with(Source.delete_source_response_model,
                        code=HTTPStatus.OK,
                        description='Delete source',
                        skip_none=True)
    def delete(self, source_id):
        match = self.find_one(source_id)
        if match:
            db.session.delete(match)
            db.session.commit()
        return match, HTTPStatus.OK

    @ls_ns.doc(body=Source.create_source_request_resource_model, validate=True)
    @ls_ns.marshal_with(Source.update_source_response_model)
    def put(self, source_id):

        data = v1_api.payload
        updated_source = self.source_service.update_source(source_id, data)
        if updated_source:
            return updated_source, HTTPStatus.OK
        else:
            abort(HTTPStatus.BAD_REQUEST, f'source with id {source_id} does not exist')

        # payload = v1_api.payload
        # match = self.find_one(source_id)
        # # TODO refactor and check if anything changed before doing update.
        # # Probably build an object from incoming request and compare it to found in DB
        # if match is not None:
        #     match.name = payload.get('name')
        #     match.description = payload.get('description')
        #     match.link = payload.get('link')
        #     match.last_updated = datetime.utcnow()
        # else:
        #     abort(404, 'Source not found')
        # tags_to_update = self.find_tags(payload)
        # # If either of tags is not found in db, abort
        # if None in self.find_tags(payload):
        #     abort(HTTPStatus.NOT_FOUND, 'One of the tags is not found')
        # else:
        #     tags_to_delete = [tag for tag in match.tags if tag not in tags_to_update]
        #     # If there are no tags to be updated:
        #     if not (not tags_to_delete and tags_to_update == match.tags):
        #         if tags_to_delete:
        #             for t in tags_to_delete:
        #                 match.tags.remove(t)
        #         for t in tags_to_update:
        #             match.tags.append(t)
        #         db.session.commit()
        #     else:
        #         return match, HTTPStatus.OK
        # return match, HTTPStatus.OK


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
                        as_list=True,
                        description='Create new source')
    def post(self):
        data = v1_api.payload
        new_source = self.source_service.save_new_source(data)
        if new_source:
            return new_source, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.BAD_REQUEST, f'there is already a source with link {data["link"]}')
