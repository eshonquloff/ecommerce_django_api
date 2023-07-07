from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, ListSerializer


from apps.models import Category, Product, ProductImage, Cart, Brand, Favourite


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class DynamicFieldsModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existed = set(self.fields)
            for field_name in existed - allowed:
                self.fields.pop(field_name)


class CategoryModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class BrandModelSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def to_representation(self, instance):
        _repr = super().to_representation(instance)
        return _repr['image']


class ListProductModelSerializer(ModelSerializer):
    images = ListSerializer(child=ProductImageModelSerializer(), read_only=True)
    category = CategoryModelSerializer(fields=('id', 'name'), read_only=True)
    brand = BrandModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CreateCartModelSerializer(ModelSerializer):
    product = ListProductModelSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = 'user', 'product', 'product_count'


class ListCartModelSerializer(ModelSerializer):
    product = ListProductModelSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = 'product_count', 'product'


class ListFavouriteModelSerializer(ModelSerializer):
    product = ListProductModelSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = ('product',)

# class ProductDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = ProductDocument
#         fields = ('id', 'title', 'description')
