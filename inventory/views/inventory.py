""" Inventory views """

# Django rest framework
from  rest_framework import mixins, viewsets

class InventoryViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin):
    """ Inventory viewsets """
