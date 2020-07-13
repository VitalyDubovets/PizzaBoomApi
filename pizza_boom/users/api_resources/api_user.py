import flask
import structlog
from flask_restful import Resource

from pizza_boom.users.business_logic.patch_user import patch_user


logger = structlog.get_logger()


class UserAPI(Resource):
    """
    Endpoint for edit User
    
    - /api/v1/users/{id} 
    """

    @staticmethod
    def patch(user_id: str):
        json_data = flask.request.get_json(silent=True) or {}

        logger.debug(
            'user_api_patch',
            user_id=user_id,
            json_data=json_data
        )
        user_data: dict = patch_user(user_id=user_id, json_data=json_data)
        logger.debug(
            'user_model_in_api_patch',
            user_data=user_data
        )
        return {
            'user': user_data
        }, 200
