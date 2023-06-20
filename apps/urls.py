from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductListCreateAPIView, CategoryAPIView

router = DefaultRouter()
router.register('products', ProductListCreateAPIView, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryAPIView.as_view()),
]
