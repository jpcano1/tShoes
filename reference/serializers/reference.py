""" Reference serializer class """

# Django rest framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Reference Models
from reference.models import Reference

# Inventory models
from inventory.models import Inventory

class CreateReferenceSerializer(serializers.Serializer):
    """ This serializers allows me to create a Reference with bussiness logic """

    # The name of the reference
    reference_name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=Reference.objects.all())
        ],
        required=True
    )

    # The price of the reference
    price = serializers.FloatField(required=True)

    # The inventory in which the reference will be added
    inventory = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all(), required=True)

    # Minimum quantity for this reference in the inventory
    min_stock = serializers.IntegerField(required=True)

    # Maximum quantity for this reference in the inventory
    max_stock = serializers.IntegerField(required=True)

    def create(self, data):
        """ Creates the reference and adds it into an inventory """
        reference = Reference.objects.create(**data)
        return reference

    class Meta:
        """ Meta class """
        model = Reference
