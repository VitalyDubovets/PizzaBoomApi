class Config:
    CSRF_ENABLED: bool = True
    DEBUG: bool = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


