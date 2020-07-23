from time import sleep

from requests import Response

from tests.utils.api_client import UserAPIClient


class TestPizzaOrderProcesses:
    def test_create_pizza_order(self, generate_user_api_client):
        user_api: UserAPIClient = generate_user_api_client()
        json_data: dict = {
            "address": "Dom epta 33",
            "additional_phone": "+791211212122",
            "note": "Hochu jrat'",
        }

        response: Response = user_api.create_pizza_order(json_data=json_data)
        assert response.status_code == 201

        sleep(50)

        receive_response: Response = user_api.receive_pizza_order()
        assert receive_response.status_code == 200

    def test_premature_sending_to_receive_in_order(self, generate_user_api_client):
        user_api: UserAPIClient = generate_user_api_client()
        json_data: dict = {
            "address": "Dom epta 33",
            "additional_phone": "+791211212122",
            "note": "Кушац",
        }

        response: Response = user_api.create_pizza_order(json_data)
        assert response.status_code == 201

        receive_response: Response = user_api.receive_pizza_order()
        assert receive_response.status_code == 404

    def test_get_pizza_orders(self, generate_user_api_client):
        user_api: UserAPIClient = generate_user_api_client()

        response: Response = user_api.get_pizza_orders()
        assert response.status_code == 200
