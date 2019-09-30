""" References Views """

# Django rest framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    def retrieve(self, request, *args, **kwargs):
        """ Retrieves the model of the reference and if it
            asks for availability, returns a boolean
        """
        shoe = Reference.objects.get(id=kwargs['id'])
        data = ReferenceModelSerializer(shoe).data
        if request.META['QUERY_STRING']:
            quantity = request.META['QUERY_STRING'].split('=')[1]
            if shoe.stock < int(quantity):
                data = {
                    'available': 'no'
                }
            else:
                data = {
                    'available': 'yes'
                }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def quantity(self, request, *args, **kwargs):
        """ Retrieves the availability of the reference """
        shoe = Reference.objects.get(id=kwargs['id'])
        quantity = request.data['quantity']
        if shoe.stock < int(quantity):
            data = {
                'message': '0'
            }
        else:
            data = {
                'message': '1'
            }
        return Response(data, status=status.HTTP_200_OK)