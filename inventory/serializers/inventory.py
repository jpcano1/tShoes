""" Inventory Serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from inventory.models import Inventory

# Designer models
from users.models import Designer

# Reference Serializers
from reference.serializers import ReferenceModelSerializer

class CreateInventorySerializer(serializers.Serializer):
    """ Serializer that allows me to create an inventory """

    # The desginer of the inventory
    designer = serializers.PrimaryKeyRelatedField(queryset=Designer.objects.all())

    # This hidden field lets the current user create the inventory without
    # user's interaction
    # designer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Make validations on sprint 3
    # def validate(self, data):
    #     """ Respective validations: The creator is a designer  """
    #
    #     if self.context['request'].user != data['designer']:
    #         raise serializers.ValidationError("You're not allowed to create an inventory. You are not a designer")
    #
    #     return data

    def create(self, data):
        """ Creates an inventory for the shoes that are gonna be sold """
        inventory = Inventory.objects.create(**data)
        return inventory

class InventoryModelSerializer(serializers.ModelSerializer):
    """ This serializer represents the model of the inventory """

    # The desginer of the inventory
    designer = serializers.StringRelatedField(read_only=True)

    # The references of the inventory
    references = ReferenceModelSerializer(many=True, read_only=True)

    class Meta:
        """ Meta class """
        model = Inventory
        fields = '__all__'