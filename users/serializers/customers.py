""" Customers Serializers """

# Django rest framework
from rest_framework import serializers

# Users Serializers
from .users import UserSignUpSerializer

# Customer models
from ..models import Customer

# Serializers
from .users import UserModelSerializer

class CustomerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up customer model,
        allows me to create new customers
    """

    # Basic data about localization: billind_address, city, country and zip code.
    billing_address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=255)

    def validate(self, data):
        super(CustomerSignUpSerializer, self).validate(data)
        return data

    def create(self, data):
        """  """
        data.pop('password_confirmation')
        customer = Customer.objects.create(**data)
        return customer

class CustomerModelSerializer(serializers.ModelSerializer):
    """  """

    class Meta:
        model = Customer
        fields = UserModelSerializer.Meta.fields.copy()
        fields.append('billing_address')
        fields.append('city')
        fields.append('country')
        fields.append('zip_code')
