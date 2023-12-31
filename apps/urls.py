from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.views import ProductModelViewSet, CategoryAPIView, CartAPIView, FavouriteAPIView

router = DefaultRouter()
# router.register('search/products', ProductDocumentView, basename='search_products')
router.register('products', ProductModelViewSet, basename='products')
router.register('users/carts', CartAPIView, basename='users_carts')
router.register('users/favourites', FavouriteAPIView, basename='users_favourites')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
