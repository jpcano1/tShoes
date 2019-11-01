""" Designers Viewset """

# Django rest framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

# User Serializers
from ..serializers import (DesignerSignUpSerializer,
                               DesignerModelSerializer)

# Inventory Serializers
from inventory.serializers import (InventoryModelSerializer,
                                   CreateInventorySerializer)

# Reference Serializers
from reference.serializers import (CreateReferenceSerializer,
                                   ReferenceModelSerializer)

# Designer Models
from users.models import Designer

# Inventory Models
from inventory.models import Inventory

# Reference models
from reference.models import Reference

# Permissions
from ..permissions import (IsAccountOwner,
                           IsDesigner,
                           IsInventoryOwner,
                           IsReferenceOwner)

class DesignersViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin):
    """ The viewset of the designers """

    queryset = Designer.objects.all()
    serializer_class = DesignerModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = []
        if self.action in ['create']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAccountOwner]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """ Sends the information to the serializer to make the respective
         verification of the data and then the creation """
        serializer = DesignerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        designer = serializer.save()
        data = DesignerModelSerializer(designer).data
        return Response(data, status=status.HTTP_201_CREATED)

class DesignerInventoryViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,):
    """ The viewset to CRUD and inventory from a specific designer """

    serializer_class = InventoryModelSerializer
    queryset = Inventory.objects.all()

    def get_permissions(self):
        permissions = [IsAuthenticated, IsDesigner]
        if self.action in ['retrieve']:
            permissions.append(IsInventoryOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """ obtains the designer from the keyword 'designer' in the url """
        id = kwargs['designer']
        self.designer = get_object_or_404(
            Designer,
            id=id
        )
        return super(DesignerInventoryViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """ Lists the inventorie of the designer """
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
        """ Creates the inventory of the designer """
        designer = self.designer
        request.data['designer'] = designer.id
        serializer = CreateInventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inventory = serializer.save()
        data = InventoryModelSerializer(inventory).data
        return Response(data, status=status.HTTP_201_CREATED)

class DesignerReferenceViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin):
    """ Viewset of the relationship designer - inventory - reference """

    queryset = Reference.objects.all()
    serializer_class = ReferenceModelSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        permissions = [IsAuthenticated, IsDesigner]
        if self.action in ['update', 'destroy', 'partial_update']:
            permissions.append(IsReferenceOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """ Retrieves the desginer and its respective inventory """
        designer_id = kwargs['designer']
        inventory_id = kwargs['inventory']
        self.designer = get_object_or_404(
            Designer,
            id=designer_id)
        self.inventory = get_object_or_404(
            Inventory,
            id=inventory_id,
            designer=designer_id
        )
        return super(DesignerReferenceViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Creates the reference from the inventory that was found """
        inventory = self.inventory
        data = request.data.copy()
        data['inventory'] = inventory.id
        serializer = CreateReferenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        reference = serializer.save()
        data = ReferenceModelSerializer(reference).data
        return Response(data, status=status.HTTP_201_CREATED)