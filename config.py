class Config:
    """
        Flask app config
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SWAGGER_DOC_PATH = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://source:secret@localhost/source'
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_DOC_PATH = '/doc/'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_DOC_PATH = '/doc/'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
