""" Bill urls """
# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import bill as bill_views

router = DefaultRouter()
router.register(r'bills', bill_views.BillViewSet, basename='bill')

urlpatterns = [
    path('', include(router.urls))
]