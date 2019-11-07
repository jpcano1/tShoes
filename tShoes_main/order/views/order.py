""" Order views """

# Django rest framework
from rest_framework import viewsets, mixins, status

# Models
from ..models import Order

# Serializers
from ..serializers import OrderModelSerializer

class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    """ Order view set """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    lookup_field = 'id'