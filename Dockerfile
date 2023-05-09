# Dockerfile

# 베이스 이미지로 Python 3.9 이미지를 사용합니다.
FROM python:3.9

# 작업 디렉토리를 /room_escape_api 설정합니다.
WORKDIR /room_escape_api

# 필요한 파일들을 Docker 이미지에 복사합니다.
COPY requirements.txt .
COPY branches branches
COPY brands brands
COPY common common
COPY config_django config_django
COPY reviews reviews
COPY rooms rooms
COPY users users
COPY wishlists wishlists
COPY db.sqlite3 .
COPY manage.py .
COPY .gitignore .

# .git 디렉토리를 제외합니다.
RUN rm -rf .git

# 필요한 Python 라이브러리를 설치합니다.
RUN pip install -r requirements.txt

# 애플리케이션을 실행합니다.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# docker run --env-file .env --rm -p 0.0.0.0:8000:8000 room_escape_api
