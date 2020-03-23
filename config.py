class Config:
    """
        Flask app config
    """
    DEBUG = False
    TESTING = False
    MONGOALCHEMY_CONNECTION_STRING = ''
    SWAGGER_DOC_PATH = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGOALCHEMY_CONNECTION_STRING = ''
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_DOC_PATH = '/doc/'


class TestingConfig(Config):
    TESTING = True
    MONGOALCHEMY_CONNECTION_STRING = ''


class ProductionConfig(Config):
    MONGOALCHEMY_CONNECTION_STRING = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
