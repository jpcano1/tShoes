""" Reference Views """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import references as reference_views
from .views import item as item_views

router = DefaultRouter()
router.register(r'references', reference_views.ReferenceViewSet, basename='reference')
router.register(r'references/(?P<reference>[0-9]+)/item', item_views.ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls))
]