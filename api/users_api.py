import logging

from api.base_client import BaseClient
from api.mapper import user_dataclass_to_payload

logger = logging.getLogger(__name__)


class UserEndpoints:
    CREATE_USER = "/api/createAccount"
    GET_USER_BY_EMAIL = "/api/getUserDetailByEmail"
    UPDATE_USER_ACCOUNT = "/api/updateAccount"
    DELETE_USER_ACCOUNT = "/api/deleteAccount"
    VERIFY_USER_LOGIN = "/api/verifyLogin"


class UsersApi:
    def __init__(self, client: BaseClient):
        self._client = client

    def create_user(self, user_data):
        logger.info(f"Creating user: {user_data}")
        payload = user_dataclass_to_payload(user_data)
        return self._client.post(UserEndpoints.CREATE_USER, data=payload)

    def update_user(self, user_data, headers=None):
        logger.info(f"Updating user: {user_data}")
        payload = user_dataclass_to_payload(user_data)
        return self._client.put(
            UserEndpoints.UPDATE_USER_ACCOUNT, json=payload, headers=headers
        )

    def get_user_by_email(self, email, headers=None):
        logger.info(f"Getting user: {email}")
        return self._client.get(
            UserEndpoints.GET_USER_BY_EMAIL, params={"email": email}, headers=headers
        )

    def verify_login(self, email, password, headers=None):
        logger.info(f"Verifying user: {email}")
        return self._client.post(
            UserEndpoints.VERIFY_USER_LOGIN,
            json={"email": email, "password": password},
            headers=headers,
        )

    def delete_user(self, email, password, headers=None):
        logger.info(f"Deleting user: {email}")
        return self._client.delete(
            UserEndpoints.DELETE_USER_ACCOUNT,
            json={"email": email, "password": password},
            headers=headers,
        )
