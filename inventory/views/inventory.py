""" Inventory views """

# Django rest framework
from  rest_framework import mixins, viewsets, status
from rest_framework.response import Response

# Models
from inventory.models import Inventory

# Serializers
from inventory.serializers import InventoryModelSerializer

class InventoryViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    """ Inventory viewsets """

    queryset = Inventory.objects.all()
    serializer_class = InventoryModelSerializer
    lookup_field = 'id'