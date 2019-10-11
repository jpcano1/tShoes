""" Bill serializers """

# Django settings
from django.conf import settings

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

# Twilio
from twilio.rest import Client

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
        self.send_order_confirmation(bill)
        return bill

    def send_order_confirmation(self, bill):
        """
            Sends the verification of the order
            :param bill: the bill to be sent
        """
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = "Your order {} has been placed: \n".format(bill.order.id)
        message += "id: {} \n".format(bill.id)
        message += "items: \n"
        for item in bill.order.items.all():
            message += "id: {}\n".format(item.reference.id)
            message += "name: {} \n".format(item.reference.reference_name)
            message += "designer: {} \n".format(item.reference.inventory.designer.get_full_name())
        message += "total price: {} \n".format(bill.total_price)
        message += "Thanks for buying with tShoes"
        try:
            client.messages.create(body=message,
                                   from_=settings.FROM_NUMBER,
                                   to=bill.order.customer.phone_number)
        except:
            raise serializers.ValidationError("There was an error processing your request")

        designers = {}
        # message = "The customer {} has bought these articles: \n".format(bill.order.customer.get_full_name())
        for item in bill.order.items.all():
            message = "id: {}\n".format(item.reference.id)
            message += "name: {} \n".format(item.reference.reference_name)
            message += "from inventory: {} \n".format(item.reference.inventory.id)
            message += "quantity: {} \n".format(item.quantity)
            if designers.get(item.reference.inventory.designer.id):
                designers[item.reference.inventory.designer.id]['message'] += message
            else:
                message += "bought by: {} \n".format(bill.order.customer.get_full_name())
                data = {
                    "message": message,
                    "phone": item.reference.inventory.designer.phone_number
                }
                designers[item.reference.inventory.designer.id] = data
        try:
            for value in designers.values():
                client.messages.create(body=value['message'],
                                       from_=settings.FROM_NUMBER,
                                       to=value['phone'])
        except:
            raise serializers.ValidationError("There was an error processing your request")

class BillModelSerializer(serializers.ModelSerializer):
    """ Bill Model Serializer """

    # The order related to the bill
    order = OrderModelSerializer(read_only=True)
    class Meta:
        """ Meta Class """
        model = Bill
        fields = '__all__'

