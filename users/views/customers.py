""" Customer views """

# Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

# Customer models
from ..models import Customer

# Customer Serializers
from ..serializers import CustomerModelSerializer

class CustomerViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    """ Documentar """
    queryset = Customer.objects.all()
    serializer_class = CustomerModelSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        """ Documentar """
        serializer = CustomerModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        data = CustomerModelSerializer(customer).data
        return Response(data, status=status.HTTP_201_CREATED)