from http import HTTPStatus

from flask_restplus import Resource, Namespace, abort

from app.exceptions import FieldValidationException
from ..model.learning_source import *

ls_ns = Namespace('ls')


@ls_ns.route('/sources/<int:source_id>')
class LearningSource(Resource):

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
        payload = v1_api.payload
        match = self.find_one(source_id)
        # TODO refactor and check if anything changed before doing update.
        if match is not None:
            match.name = payload.get('name')
            match.description = payload.get('description')
            match.link = payload.get('link')
            match.last_updated = datetime.utcnow()
        else:
            abort(404, 'Source not found')
        tags_to_update = self.find_tags(payload)
        # If either of tags is not found in db, abort
        if None in self.find_tags(payload):
            abort(HTTPStatus.NOT_FOUND, 'One of the tags is not found')
        else:
            tags_to_delete = [tag for tag in match.tags if tag not in tags_to_update]
            # If there are no tags to be updated:
            if not (not tags_to_delete and tags_to_update == match.tags):
                if tags_to_delete:
                    for t in tags_to_delete:
                        match.tags.remove(t)
                for t in tags_to_update:
                    match.tags.append(t)
                db.session.commit()
            else:
                return match, HTTPStatus.OK
        return match, HTTPStatus.OK


@ls_ns.route('/')
class LearningSourceList(Resource):
    @ls_ns.marshal_with(Source.get_sources_response_resource_model,
                        code=HTTPStatus.OK,
                        as_list=True,
                        description='Get all sources',
                        envelope='sources')
    def get(self):
        sources = Source.query.all()
        return sources, HTTPStatus.OK

    @ls_ns.doc(body=Source.create_source_request_resource_model, validate=True)
    @ls_ns.marshal_with(Source.create_source_response_resource_model,
                        code=HTTPStatus.CREATED,
                        as_list=True,
                        description='Create new source')
    def post(self):
        payload = v1_api.payload
        exception_map = {}
        not_found_tags = []
        tags = []
        request_tags = [x.lower() for x in [tag['name'] for tag in payload['tags']]]

        # Verify if tags are present in db and populate list of tags to add to source
        for tag in request_tags:
            existing_tag = Tag.query.filter_by(name=tag).first()
            if existing_tag:
                tags.append(existing_tag)
            else:
                not_found_tags.append(tag.name)
        if not_found_tags:
            exception_map['tag_not_found'] = not_found_tags

        # Duplicates check
        # TODO do some modifications to url before checking for duplicate
        existing_source = Source.query.filter_by(link=payload['link']).first()
        if existing_source:
            exception_map['duplicate_source'] = f'Source from `{payload["link"]}` already exists.'

        if exception_map:
            raise FieldValidationException(exception_map=exception_map)
        else:
            # TODO insert urls if the same format
            new_source = Source(name=payload.get('name'),
                                description=payload.get('description'),
                                link=payload.get('link'),
                                created_at=datetime.utcnow(),
                                last_updated=datetime.utcnow())
            for t in tags:
                new_source.tags.append(t)
            db.session.add(new_source)
            db.session.commit()
            return new_source, HTTPStatus.CREATED
