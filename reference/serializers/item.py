""" Item serializer """

# Django rest framework
from rest_framework import serializers

# Item models
from ..models import Item, Reference

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

    quantity = serializers.IntegerField()

    reference = serializers.PrimaryKeyRelatedField(queryset=Reference.objects.all())

    def validate(self, data):
        try:
            user = data['user']
            order = Order.objects.get(customer=user, status=Status.NONE)
            self.context['order'] = order
        except (Order.DoesNotExist, KeyError):
            pass
        return data

    def create(self, data):
        order = self.context.get('order')
        reference = data['reference']
        quantity = data['quantity']
        if order:
            item = Item.objects.create(
                order=order,
                reference=reference,
                quantity=quantity
            )
            return item
        order = Order.objects.create()
        item = Item.objects.create(
                order=order,
                reference=reference,
                quantity=quantity
            )
        return item


