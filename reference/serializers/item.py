""" Item serializer """

# Django rest framework
from rest_framework import serializers

# Item models
from ..models import Item

# Order models
from order.models import Order, Status

class ReferenceField(serializers.RelatedField):
    """ Reference personalized field """

    def to_representation(self, value):
        """  """
        data = {
            'id': value.id,
            'inventory': value.inventory,
            'price': value.price,
            'reference_name': value.reference_name
        }
        return data

class OrderField(serializers.RelatedField):
    """ Order related field """
    # Pendiente


class ItemModelSerializer(serializers.ModelSerializer):
    """ Item model serializer """

    reference = ReferenceField(read_only=True)

    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """ Meta Class """
        model = Item
        exclude = ('created', 'modified')
        ordering = ('-created', '-modified')

class AddItemSerializer(serializers.Serializer):

    def validate(self, data):
        user = data['user']

        try:
            order = Order.objects.get(customer=user, status=Status.NONE)
            self.context['order'] = order
        except Order.DoesNotExist:
            pass
        return data

    def create(self, data):
        print(data)
        # order = self.context['order']
        # reference = data['reference']
        # quantity = data['quantity']
        # if order.exists():
        #     item = Item.objects.create(
        #         order=order,
        #         reference=reference,
        #         quantity=quantity
        #     )
        #     return item
        # user = data['user']
        # order = Order.objects.create()
        # item = Item.objects.create(
        #         order=order,
        #         reference=reference,
        #         quantity=quantity
        #     )
        # return item
        return "Hola"


