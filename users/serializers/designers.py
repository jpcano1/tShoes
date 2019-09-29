""" Designer Serializer """
# Django Rest framework
from rest_framework import serializers

# Serializer
from .users import UserSignUpSerializer

# Invetory Serializers
from inventory.serializers import InventoryModelSerializer

# Models
from users.models import Designer


class DesignerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up designer model, allows me to create new designers """

    # Order address of the designer, where the reference is picked up
    order_address = serializers.CharField(max_length=255)

    def validate(self, data):
        super(DesignerSignUpSerializer, self).validate(data)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        designer = Designer.objects.create(**data)
        return designer

class DesignerModelSerializer(serializers.ModelSerializer):
    """ The model serializer of designers """

    # Inventory of the designer
    inventory = InventoryModelSerializer(read_only=True)

    class Meta:
        """ Meta class """
        model = Designer
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'identification',
                  'order_address',
                  'inventory',)
