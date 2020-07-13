from typing import Any

import structlog
from flask_restful import Resource, reqparse

from pizza_boom.users.business_logic.patch_user import patch_user


logger = structlog.get_logger()


class UserAPI(Resource):
    """
    Endpoint for edit User
    
    - /api/v1/users/{id} 
    """
    def __init__(self):
        self.parser: Any = reqparse.RequestParser()
        self.parser.add_argument('first_name', type=str, location='json')
        self.parser.add_argument('last_name', type=str, location='json')
        self.parser.add_argument('phone', type=str, location='json')
        super(UserAPI, self).__init__()

    def patch(self, user_id: str):
        user_patch_data: dict = self.parser.parse_args()

        logger.debug(
            'user_api_patch',
            user_id=user_id,
            data=user_patch_data
        )

        user_data: dict = patch_user(
            user_id=user_id, user_patch_data=user_patch_data
        )

        logger.debug(
            'user_model_in_api_patch',
            user_data=user_data
        )
        return {
            'user': user_data
        }, 200
