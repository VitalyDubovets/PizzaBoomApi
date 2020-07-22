from tests.utils.api_client import UserAPIClient


class TestUser:
    def test_patch_user_valid(self, cognito_idp_client, generate_user_api_client):
        user_api: UserAPIClient = generate_user_api_client()
        json_data: dict = {
            'first_name': user_api.user.first_name,
            'last_name': user_api.user.last_name,
            'phone': user_api.user.phone,
        }

        response = user_api.patch_user(
            json_data=json_data
        )

        assert response.status_code == 200
