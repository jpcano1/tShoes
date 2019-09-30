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
from ..serializers import ItemModelSerializer

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
        print(request.user)
        print(request.data)
        return Response("Hola", status=status.HTTP_201_CREATED)