""" Order views """

# Django rest framework
from rest_framework import viewsets, mixins, status

# Models
from ..models import Order

# Serializers
from ..serializers import OrderModelSerializer

class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin):
    """ Order view set """

    serializer_class = OrderModelSerializer
    lookup_field = 'id'