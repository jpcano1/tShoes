""" Order Urls """

# Django models
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Order views
from .views import order as order_views

# Router manager of the urls
router = DefaultRouter()
router.register(r'orders', order_views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls))
]