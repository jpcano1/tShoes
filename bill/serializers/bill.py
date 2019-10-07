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

    # The order related to the bill
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    def validate_order(self, data):
        """ :param data: is the order to be validated
            :exception: if the order is placed, generates exception
            :return: data validated
        """
        if data.status != 0:
            raise serializers.ValidationError('The order is placed')
        return data

    def create(self, data):
        """ :param data: the data that is going to be passed to the
            Bill model to be created
            :return: the bill created after the entire process
        """
        # Total cost of the order
        total = 0
        order = data['order']
        # All the items in the order
        items = Item.objects.filter(order=order)
        for item in items:
            reference = item.reference
            if reference.stock < item.quantity:
                raise serializers.ValidationError("There are not enough references of this product: {}".format(str(reference)))
            reference.stock -= item.quantity
            total += item.quantity * reference.price
            reference.save()
        # Changes the status of the order
        order.status = 1
        order.save()
        bill = Bill.objects.create(order=order, total_price=total)
        return bill

class BillModelSerializer(serializers.ModelSerializer):
    """ Bill Model Serializer """

    # The order related to the bill
    order = OrderModelSerializer(read_only=True)
    class Meta:
        """ Meta Class """
        model = Bill
        fields = '__all__'

