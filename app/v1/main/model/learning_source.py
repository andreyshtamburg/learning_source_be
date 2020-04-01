from datetime import datetime
from app import db


source_tag = db.Table('source_tag',
                      db.Column('source_id', db.Integer, db.ForeignKey('sources.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                      db.PrimaryKeyConstraint('source_id', 'tag_id'))


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)


class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(512), nullable=False)
    tags = db.relationship('Tag', secondary=source_tag, backref='sources')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<{__name__}.{__class__} id: {self.id}>'
