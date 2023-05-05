from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_406_NOT_ACCEPTABLE,
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Room
from branches.models import Branch
from .serializers import RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer


# Create your views here.
class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            branch_pk = request.data.get("branch")

            if not branch_pk:
                raise ParseError("Branch is required.")

            try:
                branch = Branch.objects.get(pk=branch_pk)
            except Branch.DoesNotExist:
                raise ParseError("Branch not found.")

            room = serializer.save(branch=branch)
            serializer = RoomDetailSerializer(
                room, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_room = serializer.save()
            return Response(
                RoomDetailSerializer(
                    updated_room, context={"request": request}
                ).data,
                status=HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()

        return Response({"ok": "방이 성공적으로 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],  # 노션 노트 참조.
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class RoomFilters(APIView):
    def append_rooms_by_avg_score(self, score_type, param2value, room_obj):
        min_avg_score_type_key = f"min_avg_{score_type}"
        max_avg_score_type_key = f"max_avg_{score_type}"
        reviews_score_type_accessors = f"reviews__{score_type}"

        if (
            min_avg_score_type_key in param2value
            and max_avg_score_type_key in param2value
        ):
            min_avg = float(param2value[min_avg_score_type_key])
            max_avg = float(param2value[max_avg_score_type_key])
            room_obj = room_obj.annotate(
                avg=Avg(reviews_score_type_accessors)
            ).filter(avg__gte=min_avg, avg__lte=max_avg)
        elif min_avg_score_type_key in param2value:
            min_avg = float(param2value[min_avg_score_type_key])
            room_obj = room_obj.annotate(
                avg=Avg(reviews_score_type_accessors)
            ).filter(avg__gte=min_avg)
        elif max_avg_score_type_key in param2value:
            max_avg = float(param2value[max_avg_score_type_key])
            room_obj = room_obj.annotate(
                avg=Avg(reviews_score_type_accessors)
            ).filter(avg__lte=max_avg)

        return room_obj

    def append_rooms_by_time_duration(self, param2value, room_obj):
        min_time_duration_key = "min_time_duration"
        max_time_duration_key = "max_time_duration"

        if (
            min_time_duration_key in param2value
            and max_time_duration_key in param2value
        ):
            room_obj = room_obj.filter(
                time_duration__gte=param2value[min_time_duration_key],
                time_duration__lte=param2value[max_time_duration_key],
            )
        elif min_time_duration_key in param2value:
            room_obj = room_obj.filter(
                time_duration__gte=param2value[min_time_duration_key]
            )
        elif max_time_duration_key in param2value:
            room_obj = room_obj.filter(
                time_duration__lte=param2value[max_time_duration_key]
            )

        return room_obj

    def get(self, request):
        param2value = dict()
        for key, val in request.query_params.items():
            param2value[key] = val

        room_obj = Room.objects

        if "city" in param2value:
            city_list = param2value["city"].split(",")
            room_obj = room_obj.filter(branch__city__in=city_list)
        if "district" in param2value:
            district_list = param2value["district"].split(",")
            room_obj = room_obj.filter(branch__district__in=district_list)
        if "difficulty" in param2value:
            difficulty_list = param2value["difficulty"].split(",")
            room_obj = room_obj.filter(difficulty__in=difficulty_list)
        if "fear_degree" in param2value:
            fear_degree_list = param2value["fear_degree"].split(",")
            room_obj = room_obj.filter(fear_degree__in=fear_degree_list)
        if "activity" in param2value:
            activity_list = param2value["activity"].split(",")
            room_obj = room_obj.filter(activity__in=activity_list)

        room_obj = self.append_rooms_by_avg_score(
            "rating", param2value, room_obj
        )
        room_obj = self.append_rooms_by_avg_score(
            "interior_score", param2value, room_obj
        )
        room_obj = self.append_rooms_by_avg_score(
            "story_score", param2value, room_obj
        )
        room_obj = self.append_rooms_by_avg_score(
            "problem_score", param2value, room_obj
        )
        room_obj = self.append_rooms_by_avg_score(
            "equipment_score", param2value, room_obj
        )
        room_obj = self.append_rooms_by_avg_score(
            "creativity_score", param2value, room_obj
        )

        room_obj = self.append_rooms_by_time_duration(param2value, room_obj)

        if "brand_name" in param2value:
            room_obj = room_obj.filter(
                branch__brand__name__contains=param2value["brand_name"]
            )
        if "branch_name" in param2value:
            room_obj = room_obj.filter(
                branch__name__contains=param2value["branch_name"]
            )
        if "name" in param2value:
            room_obj = room_obj.filter(name__contains=param2value["name"])
        if "genre" in param2value:
            room_obj = room_obj.filter(genre__contains=param2value["genre"])

        serializer = RoomListSerializer(room_obj, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
