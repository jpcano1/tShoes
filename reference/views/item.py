""" Item views """

# Django models

# Django rest framwork
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Order models
from order.models import Order

# Reference models
from ..models import Reference

# Item serializer
from ..serializers import ItemModelSerializer, AddItemSerializer

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,):
    """ Item Viewset """

    serializer_class = ItemModelSerializer
    lookup_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        reference_id = kwargs['reference']
        self.reference = get_object_or_404(
            Reference,
            id=reference_id
        )
        return super(ItemViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['reference'] = self.reference.id
        serializer = AddItemSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        data = ItemModelSerializer(item).data
        return Response(data, status=status.HTTP_201_CREATED)