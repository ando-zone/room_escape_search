import jwt
from unittest import mock
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class UsersAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@email.com",
        )
        User.objects.create_user(
            username="testuser_1",
            password="testpassword",
            email="overlapped@email.com",
        )

    # Me Class: "/api/v1/users/me"
    def test_me_get_not_authenticated(self):
        response = self.client.get("/api/v1/users/me")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_get_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/api/v1/users/me")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "testuser@email.com")

    def test_me_put_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"email": "updated_email@email.com"}
        response = self.client.put("/api/v1/users/me", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updated_email@email.com")

    def test_me_put_not_authenticated(self):
        data = {"email": "updated_email@email.com"}
        response = self.client.put("/api/v1/users/me", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_put_bad_request_wrong_form_email(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"email": "not_an_email"}
        response = self.client.put("/api/v1/users/me", data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_me_put_bad_request_overlapped_email(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"email": "overlapped@email.com"}
        response = self.client.put("/api/v1/users/me", data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    # Users Class: "/api/v1/users/"
    def test_create_user(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@email.com",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "newuser@email.com")
        self.assertTrue(User.objects.filter(username="newuser").exists())

        user = User.objects.get(username="newuser")
        self.assertTrue(user.check_password("newpassword"))

    def test_create_user_no_password(self):
        data = {
            "username": "newuser",
            "email": "newuser@email.com",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_data(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "invalid_email",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    # PublicUser Class: "/api/v1/users/@<str:username>"
    def test_get_public_user(self):
        response = self.client.get("/api/v1/users/@testuser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "testuser@email.com")

    def test_get_public_user_not_found(self):
        response = self.client.get("/api/v1/users/@nonexistentuser")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # LogIn class: "/api/v1/users/log-in"
    def test_login_success(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/api/v1/users/log-in", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post("/api/v1/users/log-in", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_username(self):
        data = {"password": "testpassword"}
        response = self.client.post("/api/v1/users/log-in", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        data = {"username": "testuser"}
        response = self.client.post("/api/v1/users/log-in", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # LogOut class: "/api/v1/users/log-out"
    def test_logout_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post("/api/v1/users/log-out")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_authenticated(self):
        response = self.client.post("/api/v1/users/log-out")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # JWTLogIn class: "/api/v1/users/jwt-login"
    @mock.patch("users.views.settings")
    def test_jwt_login_success_with_mocked_secret_key(self, mock_settings):
        mock_secret_key = "mocked_secret_key"
        mock_settings.SECRET_KEY = mock_secret_key

        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/api/v1/users/jwt-login", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify token with mocked secret key
        token = response.data["token"]
        decoded_payload = jwt.decode(
            token, mock_secret_key, algorithms=["HS256"]
        )
        self.assertEqual(decoded_payload["pk"], self.user.pk)

    # GithubLogIn class: "/api/v1/users/github"
    @mock.patch("users.views.requests.post")
    @mock.patch("users.views.requests.get")
    @mock.patch("users.views.login")
    def test_github_login_success_with_new_account_created(
        self, mock_login, mock_requests_get, mock_requests_post
    ):
        mock_requests_post.return_value.json.return_value = {
            "access_token": "mock_access_token"
        }
        mock_requests_get.return_value.json.side_effect = [
            {
                "login": "github_user",
                "email": "github_user@email.com",
                "name": "Github User",
                "avatar_url": "https://example.com/avatar.png",
            },
            [{"email": "github_user@email.com"}],
        ]

        response = self.client.post(
            "/api/v1/users/github", {"code": "mock_code"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_user = User.objects.get(username="github_user")
        mock_login.assert_called_once_with(mock.ANY, created_user)

    @mock.patch("users.views.requests.post")
    @mock.patch("users.views.requests.get")
    @mock.patch("users.views.login")
    def test_github_login_success_with_existed_account(
        self, mock_login, mock_requests_get, mock_requests_post
    ):
        existed_user = User.objects.create_user(
            username="github_user",
            email="github_user@email.com",
        )
        mock_requests_post.return_value.json.return_value = {
            "access_token": "mock_access_token"
        }
        mock_requests_get.return_value.json.side_effect = [
            {
                "login": "github_user",
                "email": "github_user@email.com",
                "name": "Github User",
                "avatar_url": "https://example.com/avatar.png",
            },
            [{"email": "github_user@email.com"}],
        ]

        response = self.client.post(
            "/api/v1/users/github", {"code": "mock_code"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_login.assert_called_once_with(mock.ANY, existed_user)

    # KakaoLogIn class: "/api/v1/users/kakao"
    @mock.patch("users.views.requests.post")
    @mock.patch("users.views.requests.get")
    @mock.patch("users.views.login")
    def test_kakao_login_success_with_new_account_created(
        self, mock_login, mock_requests_get, mock_requests_post
    ):
        mock_requests_post.return_value.json.return_value = {
            "access_token": "mock_access_token"
        }
        mock_requests_get.return_value.json.return_value = {
            "kakao_account": {
                "profile": {
                    "nickname": "kakao_user",
                    "profile_image_url": "https://example.com/avatar.png",
                },
                "email": "kakao_user@email.com",
            }
        }

        response = self.client.post(
            "/api/v1/users/kakao", {"code": "mock_code"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_user = User.objects.get(username="kakao_user")
        mock_login.assert_called_once_with(mock.ANY, created_user)

    @mock.patch("users.views.requests.post")
    @mock.patch("users.views.requests.get")
    @mock.patch("users.views.login")
    def test_kakao_login_success_with_existed_account(
        self, mock_login, mock_requests_get, mock_requests_post
    ):
        existed_user = User.objects.create_user(
            username="kakao_user",
            email="kakao_user@email.com",
        )
        mock_requests_post.return_value.json.return_value = {
            "access_token": "mock_access_token"
        }
        mock_requests_get.return_value.json.return_value = {
            "kakao_account": {
                "profile": {
                    "nickname": "kakao_user",
                    "profile_image_url": "https://example.com/avatar.png",
                },
                "email": "kakao_user@email.com",
            }
        }

        response = self.client.post(
            "/api/v1/users/kakao", {"code": "mock_code"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_login.assert_called_once_with(mock.ANY, existed_user)


# ChangePassword Class: "/api/v1/users/change-password"
class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@email.com",
        )
        self.url = "/api/v1/users/change-password"
        self.client.login(username="testuser", password="testpassword")

    def test_change_password_success(self):
        data = {"old_password": "testpassword", "new_password": "newpassword"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify password has been changed
        user = User.objects.get(username="testuser")
        self.assertTrue(user.check_password("newpassword"))

    def test_change_password_incorrect_old_password(self):
        data = {"old_password": "wrongpassword", "new_password": "newpassword"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify password hasn't changed
        user = User.objects.get(username="testuser")
        self.assertTrue(user.check_password("testpassword"))

    def test_change_password_no_old_password(self):
        data = {"new_password": "newpassword"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_no_new_password(self):
        data = {"old_password": "testpassword"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_not_authenticated(self):
        self.client.logout()
        data = {"old_password": "testpassword", "new_password": "newpassword"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
