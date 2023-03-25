from rest_framework.test import APITestCase
from users.models import User


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        # 1) 유저를 생성하는 URL을 테스트할 때
        # self.client.login(
        #     username="test",
        #     password="123",
        # )

		# 2) 단지 인증만 통과하는 게 필요한 경우
        self.client.force_login(
            self.user,
        )

        response = self.client.post("/api/v1/rooms/")

        print(response.json())