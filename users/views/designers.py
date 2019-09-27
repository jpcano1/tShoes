""" Designers Viewset """

# Django rest framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

# Serializers
from users.serializers import (DesignerSignUpSerializer,
                               DesignerModelSerializer)

# Models
from users.models import Designer

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

