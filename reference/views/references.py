""" References Views """

# Django rest framework
from rest_framework import viewsets, mixins

# Reference models
from reference.models import Reference

# Reference serializers
from reference.serializers import ReferenceModelSerializer

class ReferenceViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    """ The viewset of references """

    queryset = Reference.objects.all()
    serializer_class = ReferenceModelSerializer
    lookup_field = 'id'