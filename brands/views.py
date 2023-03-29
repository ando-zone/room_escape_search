from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Brand
from .serializers import BrandSerializer


# Create your views here.
class Brands(APIView):

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)