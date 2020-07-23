import uuid
from typing import List

import boto3
import pytest
import structlog
from decouple import config

from tests.utils.api_client import UserAPIClient
from tests.utils.users import get_user_pool, User, UserPool


logger = structlog.get_logger()


@pytest.fixture(scope='module')
def cognito_idp_client():
    session = boto3.Session(
        profile_name=config("AWS_PROFILE", None),
        region_name=config("AWS_REGION", None),
    )
    cognito_idp_client = session.client("cognito-idp")
    return cognito_idp_client


@pytest.fixture(scope="module")
def user_pool(cognito_idp_client) -> UserPool:
    return get_user_pool(cognito_idp_client)


@pytest.fixture(scope='module')
def generate_user_api_client(user_pool: UserPool, cognito_idp_client):
    users: List[User] = []

    def _generate_user_api_client() -> UserAPIClient:
        user_pizza_boom: User = User(
            pool=user_pool
        )

        user_pizza_boom.register(cognito_idp_client)
        user_pizza_boom.authorize(cognito_idp_client)

        api_client: UserAPIClient = UserAPIClient(
            user=user_pizza_boom,
            cognito_idp_client=cognito_idp_client,
        )
        api_client.user.save_dynamo_user_id_to_class_attribute(
            cognito_idp_client
        )

        users.append(user_pizza_boom)
        return api_client

    yield _generate_user_api_client
    for user in users:
        user.remove(cognito_idp_client)
