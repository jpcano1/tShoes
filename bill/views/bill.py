""" Bill views """

# Django rest framework
from rest_framework import viewsets, mixins

# Bill Models
from ..models import Bill

# Serializer
from ..serializers import BillModelSerializer

class BillViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ Bill Viewset """

    queryset = Bill.objects.all()
    serializer_class = BillModelSerializer
    lookup_field = 'id'