""" Designer Serializer """
# Django Rest framework
from rest_framework import serializers

# Serializer
from .users import UserModelSerializer, UserSignUpSerializer


class DesignerSignUpSerializer(UserSignUpSerializer, serializers.Serializer)
    """  """