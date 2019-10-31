""" Order serializer """

# Django rest framework
from rest_framework import serializers

# Customer models
from users.models import Customer

# Order models
from order.models import Order

class ItemField(serializers.RelatedField):
    """ Item personalized serializer """

    def to_representation(self, value):
        """
            Method that allows me to make a representation of the field that I want to serialize
        :param value: The value that's going to be serialized
        :return: The serialized value.
        """
        reference = value.reference
        data = {
            'id': value.id,
            'quantity': value.quantity,
            'reference': {
                'id': reference.id,
                'designer': reference.inventory.designer.get_full_name()
            }
        }
        return data

class OrderModelSerializer(serializers.ModelSerializer):
    """ Order model serializer """

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    optional_address = serializers.CharField(max_length=255)
    items = ItemField(many=True, read_only=True)

    class Meta:
        """ Meta class """
        model = Order
        fields = ['id',
                  'customer',
                  'optional_address',
                  'status',
                  'items']

