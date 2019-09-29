""" Customers Serializers """

# Django rest framework
from rest_framework import serializers

# Users Serializers
from .users import UserSignUpSerializer

class CustomerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up customer model,
        allows me to create new customers
    """

