from datetime import datetime

from flask_restplus import fields

from app import db
from app.v1 import v1_api

source_tag = db.Table('source_tag',
                      db.Column('source_id', db.Integer, db.ForeignKey('sources.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                      db.PrimaryKeyConstraint('source_id', 'tag_id')
                      )


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())
    tags = db.relationship('Tag', secondary=source_tag, backref=db.backref('source_tags', lazy='dynamic'))

    tag_response_resource_model = v1_api.model('Tags', {
        'name': fields.String
    })

    get_sources_response_resource_model = v1_api.model('Sources', {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'link': fields.String,
        'tags': fields.List(fields.Nested(tag_response_resource_model)),
        'created_at': fields.DateTime,
        'last_updated': fields.DateTime
    })

    get_source_by_id_response_model = v1_api.model('Source', {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'link': fields.String,
        'tags': fields.List(fields.Nested(tag_response_resource_model)),
        'created_at': fields.DateTime,
        'last_updated': fields.DateTime
    })

    create_source_request_resource_model = v1_api.model('Create new source request model', {
        'name': fields.String,
        'description': fields.String,
        'link': fields.String,
        'tags': fields.List(fields.Nested(tag_response_resource_model)),
    })

    create_source_response_resource_model = v1_api.model('Create new source response model', {
        'id': fields.Integer,
        'name': fields.String
    })

    delete_source_response_model = v1_api.model('Delete source response model', {
        'id': fields.Integer
    })

    update_source_response_model = v1_api.model('Update source response model', {
        'id': fields.Integer,
        'last_updated': fields.DateTime
    })

    def __repr__(self):
        return f'<{__name__}.{__class__} id: {self.id}>'
