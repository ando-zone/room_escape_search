from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Branch
from .serializers import BranchSerializer


# Create your views here.
class Branches(APIView):
    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        branches = Branch.objects.all()[start:end]
        serializer = BranchSerializer(branches, many=True)

        return Response(serializer.data, status=HTTP_200_OK)