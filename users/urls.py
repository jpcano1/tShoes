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
router.register(r'users', user_views.UserViewSet)
router.register(r'designers', designer_views.DesignersViewSet, basename='designers')
router.register(r'designers/(?P<designer>[0-9]+)/inventory', designer_views.DesignerInventoryViewSet, basename='designer_inventory')
router.register(r'designers/(?P<designer>[0-9]+)/inventory/(?P<inventory>[0-9]+)/references',
                designer_views.DesignerReferenceViewSet,
                basename='designer_reference')
router.register(r'customers', customer_views.CustomerViewSet, basename='customer')
router.register(r'customers/(?P<customer>[0-9]+)/orders', customer_views.CustomerOrderViewSet, basename='customer_order')
router.register(r'customers/(?P<customer>[0-9]+)/orders/(?P<order>[0-9]+)/items',
                customer_views.CustomerItemViewSet,
                basename='customer_item')

urlpatterns = [
    path('', include(router.urls)),
    path('mail_verification/', user_views.email_verified),
    path('auth/', user_views.index),
    path('dashboard', user_views.dashboard),
    path('logout', user_views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='users:social')),
]