from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.views import ProductListCreateAPIView, CategoryAPIView

router = DefaultRouter()
router.register('products', ProductListCreateAPIView, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
