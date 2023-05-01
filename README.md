# 백엔드 API 명세서 (방탈출 평가 및 검색 서비스)

* 자세한 내용은 노션으로 확인 부탁드립니다. (추후 wiki pages를 활용하여 github에 모두 업로드 계획)

    노션 주소: https://boom-manatee-5d1.notion.site/7e071d1b0b5144f69bcd31eb73206228

## **주요 기능**

1. **방탈출 검색**: 사용자는 지역, 장르, 브랜드, 평점, 난이도, 공포도, 활동성, 인테리어, 스토리, 창의성, 문제, 장치 등 다양한 조건으로 방탈출 게임을 검색할 수 있습니다.
2. **방탈출 상세 정보 조회**: 선택된 방탈출 게임의 상세 정보를 조회할 수 있습니다. 이 정보에는 방탈출 게임의 장소를 지도로 보여주기도 하고, 여러 유저들이 해당 방탈출에 부여한 평점을 항목별로 자세하게 확인할 수 있으며 예약할 수 있는 사이트로 바로 연결해주는 링크도 제공해 줍니다.
3. **사용자 인증**: 사용자는 이메일과 비밀번호를 사용하여 로그인할 수 있으며, 회원가입 및 비밀번호 변경 기능도 제공합니다. 인증된 사용자만이 방탈출 게임에 항목 별 평가 점수 및 종합 점수를 부여할 수 있으며 사용자에 맞는 방탈출을 추천 받거나 과거 방탈출 방문 내역 조회 기능도 이용할 수 있습니다.
4. **방탈출 평가**: 사용자는 방탈출 게임에 대하여 종합적으로 점수를 부여하거나 항목(인테리어, 스토리, 창의성, 문제, 장치) 별로 점수를 부여할 수 있습니다.
5. **방탈출 내역 조회**: 사용자는 자신이 과거에 어떠한 방탈출 게임을 방문했는지 평가 내역을 바탕으로 한 번에 확인할 수 있습니다. 또한, 방문하지 않더라도 방문할 예정으로 체크한 게임들도 확인 가능합니다.

이 문서에서는 각 API 엔드포인트에 대한 명세와 사용 방법을 자세하게 설명합니다.

## ****요청 및 응답 형식****

모든 API 요청 및 응답은 JSON 형식을 사용합니다.

## 인증 및 권한

이 서비스는 사용자 인증을 위해 Django Rest Framework의 SessionAuthentication, TokenAuthentication을 사용합니다. 토큰을 이용하여 인증하는 경우, 각 API 요청 시, ‘Authorization’ 헤더에 토큰 정보를 포함시켜야 합니다.

**예시)**

```json
Authorization: Token {access_token}
```

회원 가입 시에는 이메일, 닉네임, 비밀번호가 필요하며 로그인 시에는 닉네임과 비밀번호를 사용합니다.

<details>
  <summary>인증 및 권한 관련 API EndPoint 목록 (클릭하여 목록 확인하기)</summary>
  

  * 회원 가입 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
  * 로그인 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
  * 로그아웃 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%95%84%EC%9B%83-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
  * 패스워드 변경 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C-%EB%B3%80%EA%B2%BD-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
  * 깃허브 로그인 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EA%B9%83%ED%97%88%EB%B8%8C-%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
  * 카카오 로그인 API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EC%B9%B4%EC%B9%B4%EC%98%A4-%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))
    
</details>

## ****API 엔드포인트 목록****
<details>
    <summary>rooms 모델</summary>
    
* Rooms API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* RoomDetail API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* RoomReviews API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%95%84%EC%9B%83-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* RoomFilters API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C-%EB%B3%80%EA%B2%BD-API-EndPoint-%EB%AA%A9%EB%A1%9D))
    
</details>

<details>
    <summary>wishlists 모델</summary>
    
* Wishlists API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* WishlistsDetail API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* WishlistsToggle API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%95%84%EC%9B%83-API-EndPoint-%EB%AA%A9%EB%A1%9D))
    
</details>

<details>
    <summary>brands 모델</summary>
    
* Brands API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))
    
</details>

<details>
    <summary>branches 모델</summary>
    
* Branches API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))

</details>

<details>
    <summary>users 모델</summary>
    
* Me API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%ED%9A%8C%EC%9B%90-%EA%B0%80%EC%9E%85-API-EndPoint-%EB%AA%A9%EB%A1%9D))
 
* PublicUser API EndPoint 목록 ([Link 바로가기](https://github.com/ando-zone/room_escape_search/wiki/%EB%A1%9C%EA%B7%B8%EC%9D%B8-API-EndPoint-%EB%AA%A9%EB%A1%9D))

</details>

## **EER Diagram으로 한 눈에 확인하는 model 구조**
![room_escape_diagram](https://user-images.githubusercontent.com/119149274/235348174-1ad1ba52-5268-41ec-9ba2-4c4c85ac797d.png)

