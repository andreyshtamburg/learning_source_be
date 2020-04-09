class Config:
    """
        Flask app config
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SWAGGER_DOC_PATH = '/doc/'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://source:secret@localhost/source'
    SWAGGER_UI_DOC_EXPANSION = 'list'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    SWAGGER_UI_DOC_EXPANSION = 'list'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
