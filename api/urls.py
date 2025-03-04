from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/items/buy/<int:pk>/', ItemViewSet.as_view({'get': 'buy'}), name='buy-item'),
    path('api/orders/buy/<int:pk>/', OrderViewSet.as_view({'get': 'buy'}), name='buy-order'),
]