""" Inventory Serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from inventory.models import Inventory

# Designer models
from users.models import Designer

class CreateInventorySerializer(serializers.Serializer):
    """ Serializer that allows me to create an inventory """

    # The desginer of the inventory
    designer = serializers.PrimaryKeyRelatedField(queryset=Designer.objects.all())

    def validate_designer(self, data):
        """ Validates the designer
            :param data the designer that is going to be validated
            :return: the validated data
        """
        designer = data
        q = Inventory.objects.filter(designer=designer)
        if q.exists():
            raise serializers.ValidationError("You already have an inventory")
        return data

    def create(self, data):
        """ Creates an inventory for the shoes that are gonna be sold
            :param data the data that is going to be passed to the inventory creation
            :return: the created inventory of the designer
        """
        inventory = Inventory.objects.create(**data)
        return inventory

class DesignerField(serializers.RelatedField):
    """ This is a personalized serializer for the Designer """

    def to_representation(self, value):
        """
        Transfoms the value into a serilized object
        :param value: The field that's going to be serialized
        :return: The serialized field
        """
        return value.get_full_name()

class InventoryModelSerializer(serializers.ModelSerializer):
    """ This serializer represents the model of the inventory """

    # The desginer of the inventory
    designer = DesignerField(read_only=True)

    # The references of the inventory
    references = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        """ Meta class """
        model = Inventory
        fields = '__all__'