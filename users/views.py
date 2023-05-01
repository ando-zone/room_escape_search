import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_201_CREATED,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO@Ando: request.user를 한 번 출력해보고 싶다.
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            # TODO@Ando: 패스워드 설정에서 실패해도 유저가 생성되는 문제가 발생함.(패스워드: 패스워드)
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        # TODO@Ando: PublicUserSerializer로 바꾸는 것 고민해 봅시다.
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"ok": "패스워드가 변경되었습니다."}, status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # TODO@Ando: autheticate와 login, logout에서 request는 왜 필요하고 어떻게 쓰일까?
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "로그인을 환영합니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "패스워드가 틀립니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "다음에 또 만나요!"}, status=status.HTTP_200_OK)


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=faa85bb702ec265f6120&client_secret={settings.SECRET_GITHUB}",
                # json response를 받기 위해서 json response를 요청하는 과정
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()

            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(
                    {"ok": "로그인을 환영합니다!"}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(
                    {"ok": "로그인을 환영합니다!"}, status=status.HTTP_200_OK
                )
        except Exception:
            return Response(
                {"error": "인증 코드가 유효하지 않거나, GitHub API 호출 과정에서 문제가 발생했습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "0c99f06744ebc64b48e23cbabfd95aee",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(
                    {"ok": "로그인을 환영합니다!"}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    email=kakao_account.get("email"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(
                    {"ok": "로그인을 환영합니다!"}, status=status.HTTP_200_OK
                )
        except Exception:
            return Response(
                {"error": "인증 코드가 유효하지 않거나, Kakao API 호출 과정에서 문제가 발생했습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
