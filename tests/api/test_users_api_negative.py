import pytest

ENDPOINTS_WITH_EXPECTED_METHODS = {
    "/api/createAccount": "POST",
    "/api/getUserDetailByEmail": "GET",
    "/api/updateAccount": "PUT",
    "/api/deleteAccount": "DELETE",
    "/api/verifyAccount": "POST"
    }


INVALID_METHOD_CASES = [
        pytest.param(endpoint, method, id=f"{method}-{endpoint}")
        for endpoint, expected_method in ENDPOINTS_WITH_EXPECTED_METHODS.items()
        for method in ("GET", "POST", "PUT", "DELETE", "PATCH")
        if method != expected_method
    ]

@pytest.mark.api
class TestUsersApiNegative:

    @pytest.mark.parametrize("endpoint, method", INVALID_METHOD_CASES)
    def test_unsupported_method(self, base_client, endpoint, method):
        """Endpoints must reject HTTP methods they do not support."""
        response = base_client.send(method, endpoint)
        if endpoint != "/api/getUserDetailByEmail":
            assert response.status_code == 405, (
                f"{method} {endpoint} expected 405 but got "
                f"{response.status_code}. Body: {response.text}"
            )
        else:
            assert response.status_code == 405 or base_client.body_code(response) == 405, (
                f"{method} {endpoint} expected 405 but got "
                f"{base_client.body_code(response)}. message: {response.json().get("message")}"
            )

    @pytest.mark.parametrize("invalid_payload",[
                             pytest.param({"email": "test_unique@gmail.com", "password": ""}, id="empty_password"),
                             pytest.param({"email": "testemail", "password": ""}, id="invalid_email"),
                             pytest.param({"email": "", "password": "newtest"}, id="empty_email"),]
                             )
    def test_user_creation_invalid_payload(self, invalid_payload, base_client, user_api, user_data_factory):
        """Tests invalid email and password in the payload"""
        user_data = user_data_factory(**invalid_payload)
        response = user_api.create_user(user_data)
        # this api always returns 200 status code
        assert response.status_code == 200

        #  returns actual code in response body
        assert base_client.body_code(response) in (400, 422), (
            f"Expected a validation error for {invalid_payload} but got "
            f"{response.status_code}. Body: {response.text}"
        )

