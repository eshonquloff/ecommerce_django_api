from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, ProductImage, Category
from apps.serializers import ProductModelSerializer, CategoryModelSerializer, PhotoSerializer

images_params = openapi.Parameter('images', openapi.IN_FORM, description="test manual param", type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_FILE), required=True)


class ProductListCreateAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    parser_classes = MultiPartParser, FormParser
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(tags=["products"], manual_parameters=[images_params])
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            images_list = []
            for image in images:
                images_list.append(ProductImage(image=image, product=product))
            ProductImage.objects.bulk_create(images_list)
        return Response(serializer.data)


class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


# [{ "SSD": "512", "RAM": "16" }]


