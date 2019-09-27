""" User Urls """

# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]