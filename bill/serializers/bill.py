""" Bill serializers """

# Django rest framework
from rest_framework import serializers

# Bill model
from ..models import Bill

# Order serializer
from order.serializers import OrderModelSerializer

# Item models
from reference.models import Item

# Order model
from order.models import Order

class CreateBillSerializer(serializers.Serializer):
    """ Bill model serializer """

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    def validate_order(self, data):
        """ :param data is the order to be validated
            :exception if the order is placed, generates exception
            :returns data validated """
        if data.status != 0:
            raise serializers.ValidationError('The order is placed')
        return data

    def create(self, data):
        """ :param data the data that is going to be passed to the
            Bill model to be created
            :returns the bill created after the entire process
        """
        total = 0
        order = data['order']
        items = Item.objects.filter(order=order)
        for item in items:
            reference = item.reference
            total += item.quantity * item.reference.price
            reference.stock -= item.quantity
            reference.save()
        order.status = 1
        order.save()
        bill = Bill.objects.create(order=order, total_price=total)
        return bill

class BillModelSerializer(serializers.ModelSerializer):
    """ Bill Model Serializer """

    order = OrderModelSerializer(read_only=True)
    class Meta:
        model = Bill
        fields = '__all__'

