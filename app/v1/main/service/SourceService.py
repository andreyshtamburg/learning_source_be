from datetime import datetime

from app import db
from app.v1.main.model.LearningSourceModel import Source
from app.v1.main.service.TagService import TagService

tag_service = TagService()


class SourceService:

    def save_new_source(self, data):
        exceptions = {}
        source = Source.query.filter_by(link=data['link']).first()
        if not source:
            source = Source(name=data.get('name'),
                            description=data.get('description'),
                            link=data.get('link'),
                            created_at=datetime.utcnow(),
                            last_updated=datetime.utcnow())
            self.update_tags(source, data)
            self.save_changes(source)
        else:
            exceptions['already_exist'] = f'source with link `{data.get("link")}` already exist'
        return source, exceptions

    def get_source(self, data):
        return Source.query.filter_by(link=data['link']).first()

    def get_source_by_id(self, source_id):
        return Source.query.filter_by(id=source_id).first()

    def get_all_sources(self):
        return Source.query.all()

    def tags_to_add(self, source, data):
        request_tag_names = [tag.lower() for tag in [tag['name'] for tag in data['tags']]]
        existing_tags = source.tags
        request_tags = [tag_service.get_tag_by_name(tag) for tag in request_tag_names]
        return list(set(request_tags) - set(existing_tags))

    def tags_to_delete(self, source, data):
        request_tag_names = [tag.lower() for tag in [tag['name'] for tag in data['tags']]]
        existing_tags = source.tags
        request_tags = [tag_service.get_tag_by_name(tag) for tag in request_tag_names]
        return list(set(existing_tags) - set(request_tags))

    def add_tags_for_source(self, source, data):
        tags_to_add = self.tags_to_add(source, data)
        if tags_to_add:
            for t in tags_to_add:
                source.tags.append(t)

    def remove_tags_for_source(self, source, data):
        tags_to_remove = self.tags_to_delete(source, data)
        if tags_to_remove:
            for t in tags_to_remove:
                source.tags.remove(t)

    def update_tags(self, source, data):
        exception_map = {}
        request_tags = [tag.lower() for tag in [tag['name'] for tag in data['tags']]]
        not_found_tags = [tag for tag in request_tags if tag_service.get_tag_by_name(tag) is None]
        if not_found_tags:
            exception_map['tags_not_found'] = not_found_tags
        else:
            self.remove_tags_for_source(source, data)
            self.add_tags_for_source(source, data)
        return exception_map

    def update_source(self, source_id, data):
        # TODO figure out how to return proper failure. Can be either resource not found or update link already exist.
        exception_map = {}
        if not data['link'] or data['link'].strip() == '':
            exception_map['invalid_input'] = 'Link cannot be blank'
        source = self.get_source_by_id(source_id)
        if source:
            existing_link_source = self.get_source(data)
            if not existing_link_source:
                source.name = data.get('name')
                source.description = data.get('description')
                source.link = data.get('link')
                source.last_updated = datetime.utcnow()
                self.update_tags(source, data)
                self.save_changes(source)
            else:
                exception_map['already_exist'] = f'source with link `{data.get("link")}` already exist'
        else:
            exception_map['not_found'] = f'source with id {source_id} not found'
        return source, exception_map

    def delete_source(self, source_id):
        source = self.get_source_by_id(source_id)
        if source:
            db.session.delete(source)
            db.session.commit()
            return source

    def save_changes(self, data):
        db.session.add(data)
        db.session.commit()
