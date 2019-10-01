""" Order Urls """

# Django models
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import order as order_views

router = DefaultRouter()
router.register(r'orders', order_views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls))
]