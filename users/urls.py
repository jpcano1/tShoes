""" User Urls """

# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views
from .views import designers as designer_views
from .views import customers as customer_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewset, basename='users')
router.register(r'designers', designer_views.DesignersViewSet, basename='designers')
router.register(r'designers/(?P<designer>[0-9]+)/inventory', designer_views.DesignerInventoryViewSet, basename='designer_inventory')
router.register(r'designers/(?P<designer>[0-9]+)/inventory/(?P<inventory>[0-9]+)/references',
                designer_views.DesignerReferenceViewSet,
                basename='designer_reference')
router.register(r'customers', customer_views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]