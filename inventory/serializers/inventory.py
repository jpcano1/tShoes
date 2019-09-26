""" Inventory Serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from inventory.models import Inventory

class CreateInventorySerializer(serializers.Serializer):
    """ Serializer that allows me to create an inventory """

    # This hidden field lets the current user create the inventory without
    # user's interaction
    designer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class """
        model = Inventory

    def validate(self, data):
        """ Respective validations: The creator is a designer  """

        if self.context['request'].user != data['designer']:
            raise serializers.ValidationError("You're not allowed to create an inventory. You are not a designer")

        return data

    def create(self, data):
        """ Creates an inventory for the shoes that are gonna be sold """
        designer = data['designer']
        Inventory.objects.create(designer=designer)

class InventoryModelSerializer(serializers.ModelSerializer):
    """  """


