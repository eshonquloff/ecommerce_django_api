import datetime
from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.filters import CustomProductFilter
from apps.models import Product, ProductImage, Category, Favourite, Cart, ViewHistory
from apps.serializers import CategoryModelSerializer, CreateProductModelSerializer, ListProductModelSerializer, \
    CreateCartModelSerializer, UserSerializer, ListCartModelSerializer, ListFavouriteModelSerializer

images_params = openapi.Parameter('images', openapi.IN_FORM, description="test manual param", type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_FILE), required=True)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductModelSerializer
    parser_classes = MultiPartParser, FormParser
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('title', 'brand', 'description')
    filterset_class = CustomProductFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductModelSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(tags=["products"], manual_parameters=[images_params])
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            images_list = [ProductImage(image=image, product=product) for image in images]
            ProductImage.objects.bulk_create(images_list)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def favourite(self, request, pk=None):
        try:
            Favourite.objects.get(product_id=pk, user=self.request.user).delete()
        except Favourite.DoesNotExist:
            Favourite.objects.create(product_id=pk, user=self.request.user)
        return Response({'message': 'bajarildi'}, status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, serializer_class=CreateCartModelSerializer)
    def add_cart(self, request, pk):
        product = Product.objects.get(pk=pk)
        data_product_count = request.data.get('product_count')
        if int(data_product_count) and int(data_product_count) <= product.quantity:
            cart, is_created_cart = Cart.objects.get_or_create(product=product,
                                                               user=self.request.user)
            cart.product_count = request.data.get('product_count')
            cart.save()
            return Response({'message': 'added to cart!'}, status.HTTP_201_CREATED)
        return Response({'message': 'siz qoshmoqchi bolgan mahsulot miqdorini kamaytiring'},
                        status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        data = self.get_serializer(instance).data
        ViewHistory.objects.update_or_create(product_id=kwargs.get('pk'), user=self.request.user)
        return Response(data)


class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


# [{ "SSD": "512", "RAM": "16" }]


class CartAPIView(ReadOnlyModelViewSet):
    serializer_class = ListCartModelSerializer

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart


class FavouriteAPIView(ReadOnlyModelViewSet):
    serializer_class = ListFavouriteModelSerializer

    def get_queryset(self):
        favourite = Favourite.objects.filter(user=self.request.user)
        return favourite





# class ProductDocumentView(DocumentViewSet):
#     document = ProductDocument
#     serializer_class = ProductDocumentSerializer
#
#     filter_backends = [
#         SuggesterFilterBackend
#     ]
#
#     suggester_fields = {
#         'title_suggest': {
#             'field': 'title.suggest',
#             'suggesters': [
#                 SUGGESTER_COMPLETION,
#             ],
#         },
#     }
