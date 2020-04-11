from app.v1.main.model.LearningSourceModel import Tag


class TagService:

    def get_all_tags(self):
        return Tag.query.all()

    def get_tag_by_name(self, name):
        return Tag.query.filter_by(name=name).first()
