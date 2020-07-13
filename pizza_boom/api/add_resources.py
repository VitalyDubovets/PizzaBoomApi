from flask_restful import Api

from pizza_boom.users.api_resources.api_user import UserAPI


def add_resources(api: Api):
    _add_user_resources(api)


def _add_user_resources(api: Api):
    api.add_resource(UserAPI, '/users/<user_id>', endpoint='users')
