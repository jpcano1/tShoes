""" Item serializer """

# Django rest framework
from rest_framework import serializers

# Item models
from ..models import Item, Reference

# Order models
from order.models import Order

# Customer models
from users.models import Customer

# Serializer
from ..serializers import ReferenceModelSerializer

class ReferenceField(serializers.RelatedField):
    """ Reference personalized field """

    def to_representation(self, value):
        """  """
        data = {
            'id': value.id,
            'inventory': {
                'id': value.inventory.id,
                'designer': value.inventory.designer.get_full_name()
            },
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

    def validate_quantity(self, data):
        if data <= 0:
            raise serializers.ValidationError("Choose at least one reference")
        elif data > self.context['reference'].stock:
            raise serializers.ValidationError("There are not enough references")
        return data

    class Meta:
        """ Meta Class """
        model = Item
        exclude = ('created', 'modified')
        ordering = ('-created', '-modified')

class AddItemSerializer(serializers.Serializer):
    """ Add item serializer """

    quantity = serializers.IntegerField()

    reference = serializers.PrimaryKeyRelatedField(queryset=Reference.objects.all())

    def validate_quantity(self, data):
        if data > self.context['stock']:
            raise serializers.ValidationError("There are not enough references to sell")
        elif data == 0:
            raise serializers.ValidationError("Choose at least one reference")
        return data

    def validate(self, data):
        self.context['user'] = self.context['request'].user
        try:
            user = self.context['user']
            order = Order.objects.get(customer_id=user.id, status=0)
            self.context['order'] = order
        except Order.DoesNotExist:
            pass
        try:
            item = Item.objects.get(reference=data['reference'])
            self.context['item'] = item
            if data['quantity'] + item.quantity > self.context['stock']:
                raise serializers.ValidationError("There are not enough references to sell")
            elif data['quantity'] + item.quantity < 0:
                raise serializers.ValidationError("You can't have less than 0 references")
        except Item.DoesNotExist:
            if data['quantity'] <= 0:
                raise serializers.ValidationError("Choose at least one reference")
        return data

    def create(self, data):
        reference = data['reference']
        quantity = data['quantity']
        if self.context.get('item'):
            item = self.context.get('item')
            item.quantity += quantity
            item.save()
        else:
            if self.context.get('order'):
                order = self.context.get('order')
            else:
                order = Order.objects.create(customer_id=self.context['request'].user.id)
            item = Item.objects.create(
                    order=order,
                    reference=reference,
                    quantity=quantity
                )
        return item