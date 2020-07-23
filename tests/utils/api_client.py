from typing import Optional

import backoff
import structlog
from decouple import config
from requests import Response, request

from tests.utils.users import User


logger = structlog.get_logger()


class UserAPIClient:
    def __init__(self, *, user: User, cognito_idp_client):
        self.user: User = user
        self.cognito_idp_client = cognito_idp_client
        self.domain: str = config('DOMAIN')
        self.api_version: str = config('API_VERSION', 'v1')

    @property
    def base_url(self) -> str:
        return f'https://{self.domain}/api/{self.api_version}'

    def request(
        self,
        url: str,
        json_data: dict = None,
        headers: dict = None,
        method: str = "GET",
        params: dict = None,
        **kwargs,
    ) -> Response:
        return self._request(
            url=f"{self.base_url}{url}",
            json_data=json_data,
            headers=headers,
            method=method,
            params=params,
            **kwargs,
        )

    def _request(
        self,
        url: str,
        json_data: dict = None,
        headers: dict = None,
        method: str = "GET",
        params: dict = None,
        **kwargs,
    ) -> Response:
        if headers is None:
            headers = {}

        if self.user.dynamo_user_id:
            url = url.replace("<user_id>", self.user.dynamo_user_id)

        if self.user.pizza_order_id:
            url = url.replace('<pizza_order_id>', self.user.pizza_order_id)

        base_headers = {"Content-Type": "application/json"}
        base_headers.update(headers)
        base_headers["Authorization"] = self.user.id_token

        response = request(
            method,
            url,
            headers=base_headers,
            json=json_data,
            timeout=30,
            params=params,
            **kwargs,
        )
        return response

    @backoff.on_predicate(
        backoff.constant,
        interval=2,
        predicate=lambda x: x.status_code != 200,
        max_time=20,
    )
    def patch_user(self, json_data: dict, method: str = 'PATCH') -> Response:
        return self.request(
            url='/users/<user_id>',
            json_data=json_data,
            method=method,
        )

    @backoff.on_predicate(
        backoff.constant,
        interval=2,
        predicate=lambda x: x.status_code != 201,
        max_time=20,
    )
    def create_pizza_order(self, json_data: dict, method: str = 'POST') -> Response:
        response: Response = self.request(
            url='/pizza-orders',
            json_data=json_data,
            method=method,
        )
        self.user.pizza_order_id = response.json().get('order', {}).get('id')
        return response

    @backoff.on_predicate(
        backoff.constant,
        interval=2,
        predicate=lambda x: x.status_code != 200,
        max_time=20,
    )
    def receive_pizza_order(self, method: str = 'POST') -> Response:
        return self.request(
            url='/pizza-orders/<pizza_order_id>/receive',
            method=method,
        )

    @backoff.on_predicate(
        backoff.constant,
        interval=2,
        predicate=lambda x: x.status_code != 200,
        max_time=20,
    )
    def get_pizza_orders(self, params: Optional[dict] = None) -> Response:
        return self.request(
            url='/pizza-orders',
            params=params,
        )
