""" Order serializer """

# Django rest framework
from rest_framework import serializers

# Customer models
from users.models import Customer

# Order models
from order.models import Order

class OrderModelSerializer(serializers.ModelSerializer):
    """ Order model serializer """

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    optional_adress = serializers.CharField(max_length=255)

    class Meta:
        """ Meta class """
        model = Order
        fields = ['id',
                  'customer',
                  'optional_address',
                  'references'
                  ]

