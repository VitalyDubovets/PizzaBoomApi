import os
import uuid
from dataclasses import dataclass, field
from typing import List, Optional

import backoff
import structlog
from botocore.exceptions import ClientError


logger = structlog.get_logger()


@dataclass
class UserPool:
    id: str
    client_id: str


def get_user_pool(
        cognito_idp_client,
        client_name: str = 'pizza-boom-auth-users-app'
) -> UserPool:
    user_pools: List[dict] = cognito_idp_client.list_user_pools(MaxResults=60)[
        "UserPools"
    ]
    user_pool_name = (
        f"pizza-boom-auth-{os.getenv('STAGE', 'dev')}-users-pool"
    )
    user_pool_id: str = next(
        up["Id"] for up in user_pools if up["Name"] == user_pool_name
    )
    clients: List[dict] = cognito_idp_client.list_user_pool_clients(
        UserPoolId=user_pool_id, MaxResults=60
    )["UserPoolClients"]

    client_id: str = next(
        client["ClientId"] for client in clients if client["ClientName"] == client_name
    )

    return UserPool(user_pool_id, client_id)


@dataclass
class User:
    pool: UserPool
    id_token: Optional[str] = None
    access_token: Optional[str] = None
    dynamo_user_id: Optional[str] = None
    pizza_order_id: Optional[str] = None
    email: str = 'example@test-gmail.com'
    username: str = field(default_factory=lambda: str(uuid.uuid4().hex))
    password: str = field(default_factory=lambda: str('Qwerty12'))
    first_name: str = 'first_name'
    last_name: str = 'last_name'
    phone: str = '+7123129124'
    ids_list: List[str] = field(default_factory=list)
    sub: Optional[str] = None

    @property
    def cognito_attributes(self) -> List[dict]:
        return [
            {"Name": "email", "Value": self.email},
        ]

    @backoff.on_exception(backoff.expo, ClientError, max_time=30)
    def register(self, cognito_idp_client):
        response = cognito_idp_client.sign_up(
            ClientId=self.pool.client_id,
            Username=self.username,
            Password=self.password,
            UserAttributes=self.cognito_attributes,
        )
        cognito_idp_client.admin_confirm_sign_up(
            UserPoolId=self.pool.id,
            Username=self.username
        )
        self.sub = response["UserSub"]

    @backoff.on_exception(backoff.expo, ClientError, max_time=30)
    def save_dynamo_user_id_to_class_attribute(self, cognito_idp_client) -> None:
        attributes = cognito_idp_client.admin_get_user(
            UserPoolId=self.pool.id,
            Username=self.username
        )['UserAttributes']
        self.dynamo_user_id: str = next(
            attribute['Value'] for attribute in attributes
            if attribute['Name'] == 'custom:dynamo_user_id'
        )

    def remove(self, cognito_idp_client) -> None:
        @backoff.on_exception(backoff.expo, ClientError, max_time=30)
        def _remove_user():
            cognito_idp_client.delete_user(AccessToken=self.access_token)

        try:
            _remove_user()
        except ClientError as e:
            logger.error(e)

    @backoff.on_exception(
        backoff.constant,
        interval=1,
        exception=ClientError,
        max_time=80,
    )
    def authorize(self, cognito_idp_client) -> None:
        response = cognito_idp_client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": self.username, "PASSWORD": self.password},
            ClientId=self.pool.client_id,
        )

        self.id_token = response.get("AuthenticationResult", {}).get("IdToken")

        self.access_token = response.get("AuthenticationResult", {}).get("AccessToken")
