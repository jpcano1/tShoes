""" Item serializer """

# Django rest framework
from rest_framework import serializers

# Item models
from ..models import Item, Reference

# Order models
from order.models import Order

class ReferenceField(serializers.RelatedField):
    """ Reference personalized field """

    def to_representation(self, value):
        """ Method that transforms the value into representation JSON
            :param value is the object that's going to be rendered
         """
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

class ItemModelSerializer(serializers.ModelSerializer):
    """ Item model serializer """

    # The reference related to the item
    reference = ReferenceField(read_only=True)

    # The order related to the item
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_quantity(self, data):
        """ Validate some logic to the quantity field
            :param data is the validation field
            :returns the data already validated
         """
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

    # The quantity of items of some references that are going to be bought
    quantity = serializers.IntegerField()

    # The reference to be bought
    reference = serializers.PrimaryKeyRelatedField(queryset=Reference.objects.all())

    def validate_quantity(self, data):
        """ Validates some logic of the quantity field
            :param data the data that's going to be validated
            :returns the validated data
         """
        if data > self.context['stock']:
            raise serializers.ValidationError("There are not enough references to sell")
        elif data == 0:
            raise serializers.ValidationError("Choose at least one reference")
        return data

    def validate(self, data):
        """ Validates the data that's going to be
            passed for creation of the item
            :param data the data that's going to be processed
            :returns the validated data
         """
        self.context['user'] = self.context['request'].user
        try:
            # Validates the customer already has an stateless order
            user = self.context['user']
            order = Order.objects.get(customer_id=user.id, status=0)
            self.context['order'] = order
        except Order.DoesNotExist:
            pass
        try:
            # Validates the added item already exists in the stateless order
            item = Item.objects.get(reference=data['reference'])
            self.context['item'] = item
            # Validates the number of some reference that's going to be bought
            # if data['quantity'] + item.quantity > self.context['stock']:
            #     raise serializers.ValidationError("There are not enough references to sell")
            # elif data['quantity'] + item.quantity < 0:
            #     raise serializers.ValidationError("You can't have less than 0 references")
        except Item.DoesNotExist:
            if data['quantity'] <= 0:
                raise serializers.ValidationError("Choose at least one reference")
        return data

    def create(self, data):
        """ Creates the item with the validated data
            :param data The validated data
            :returns the created item in the order
        """
        reference = data['reference']
        quantity = data['quantity']
        if self.context.get('item'):
            item = self.context.get('item')
            item.quantity = quantity
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