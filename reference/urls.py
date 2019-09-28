""" Reference Views """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import references as reference_views

router = DefaultRouter()
router.register(r'references', reference_views.ReferenceViewSet, basename='reference')

urlpatterns = [
    path('', include(router.urls))
]