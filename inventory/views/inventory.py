""" Inventory views """

# Django rest framework
from  rest_framework import mixins, viewsets

# Models
from inventory.models import Inventory

# Serializers
from inventory.serializers import InventoryModelSerializer

class InventoryViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    """ Inventory viewsets, it lists and retrieves """

    # Queryset where the queries are made
    queryset = Inventory.objects.all()
    # The serializer class of the inventory model
    serializer_class = InventoryModelSerializer
    # The field that's is going to be looked for the detail methods
    lookup_field = 'id'