""" Designers Viewset """

# Django rest framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# User Serializers
from users.serializers import (DesignerSignUpSerializer,
                               DesignerModelSerializer)

# Inventory Serializers
from inventory.serializers import (InventoryModelSerializer,
                                   CreateInventorySerializer)

# Designer Models
from users.models import Designer

# Inventory Models
from inventory.models import Inventory

# Documentar
class DesignersViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin):
    queryset = Designer.objects.all()
    serializer_class = DesignerModelSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = DesignerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        designer = serializer.save()
        data = DesignerModelSerializer(designer).data
        return Response(data, status=status.HTTP_201_CREATED)

class DesignerInventoryViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               ):
    """  """
    serializer_class = InventoryModelSerializer
    queryset = Inventory.objects.all()

    def dispatch(self, request, *args, **kwargs):
        id = kwargs['designer']
        self.designer = get_object_or_404(
            Designer,
            id=id
        )
        return super(DesignerInventoryViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        designer = self.designer
        try:
            inventory = Inventory.objects.get(designer=designer)
            data = {
                'inventory': InventoryModelSerializer(inventory).data
            }
        except Inventory.DoesNotExist:
            data = {
                'Message': "You have no inventories"
            }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        designer = self.designer
        request.data['designer'] = designer.id
        data = {}
        resp = status.HTTP_201_CREATED
        try:
            inventory = Inventory.objects.get(designer=designer)
            data = {
                'message': 'You already have an inventory'
            }
            resp = status.HTTP_403_FORBIDDEN
        except Inventory.DoesNotExist:
            serializer = CreateInventorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            inventory = serializer.save()
            data = InventoryModelSerializer(inventory).data
        return Response(data, status=resp)