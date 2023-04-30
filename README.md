<<<<<<< Updated upstream
# 백엔드 API 명세서 (방탈출 평가 및 검색 서비스)
노션 주소: https://boom-manatee-5d1.notion.site/7e071d1b0b5144f69bcd31eb73206228
=======
# room_escape_search
Find Your Type of Room Escape

### Rooms

[작성] GET[X] POST[X] /rooms
[작성] GET[X] PUT[x] DELETE[x] /rooms/1
[작성] GET[x] POST[x] PUT[] DELETE[] /rooms/1/reviews

## Wishlists

GET[x] POST[x] /wishlists
GET[x] PUT[x] DELETE[x] /wishlists/1
PUT[x] /wishlists/1/rooms/2
(Toggle 기능, 다른 방법으로 구현은 어떻게 할 수 있을까?, 
실제 프론트에서 Toggle을 이용할 걸 알고 이렇게 설계한 것인가? 결론은 프론트도 경험해야 한다.)
<!-- is_liked[] -->

## Reviews

## Brands

## Users
GET[] PUT[] /me <!-- Private view -->
POST[] /users
GET[] /users/username <!-- Public view -->
POST[] /users/log-in
POST[] /users/change-password
<!-- POST[] /users/github -->

<!-- GET[] PUT[] /me
POST[] /users
GET[] /users/@username/reviews (공개 프로필용)
POST[] /users/log-in
POST[] /users/log-out
PUT[] /users/change-password -->
>>>>>>> Stashed changes
