""" Reference Views """

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls))
]