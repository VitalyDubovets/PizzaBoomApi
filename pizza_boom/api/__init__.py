from flask import Flask
from flask_restful import Api

from pizza_boom.api.add_resources import add_resources
from pizza_boom.configs import configure_logging
from pizza_boom.users.errors import user_errors_dict


def create_app():
    configure_logging()

    errors = {
        **user_errors_dict
    }

    app: Flask = Flask(__name__)
    app.config.from_object(f'pizza_boom.configs.flask_config.DevelopmentConfig')
    api: Api = Api(app=app, prefix='/api/v1', errors=errors)
    add_resources(api)
    return app
