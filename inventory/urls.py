""" Inventory Urls """

# Django
from django.urls import include, path

# Views
from .views import inventory as inventory_views

# Django Rest framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'inventory', inventory_views.InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls))
]