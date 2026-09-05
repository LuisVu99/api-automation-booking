"""User endpoint client."""

from endpoints.base_api import BaseApi
from models.user_model import UserCreateModel, UserModel


class UserApi(BaseApi):
    """Expose user operations with typed response validation."""

    def get_user(self, user_id: int) -> UserModel:
        """Retrieve and validate one user."""
        response = self.request("GET", f"/users/{user_id}", expected_status=200)
        return UserModel.model_validate(response.json())

    def create_user(self, user: UserCreateModel) -> UserModel:
        """Create a user and validate the returned representation."""
        response = self.request("POST", "/users", json=user.model_dump(), expected_status=201)
        return UserModel.model_validate(response.json())
