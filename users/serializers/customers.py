""" Customers Serializers """

# Django rest framework
from rest_framework import serializers

# Users Serializers
from .users import UserSignUpSerializer

class CustomerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up customer model,
        allows me to create new customers
    """

    billing_adress = serializers.CharField(max_length=255)

    city = serializers.CharField(max_length=255)

    country = serializers.CharField(max_length=255)

    zip_code = serializers.CharField(max_length=255)

