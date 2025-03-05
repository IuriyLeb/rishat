from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('item/buy/<int:pk>/', ItemViewSet.as_view({'get': 'buy'}), name='buy-item'),
    path('order/buy/<int:pk>/', OrderViewSet.as_view({'get': 'buy'}), name='buy-order'),
]