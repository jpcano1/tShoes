""" Item views """

# Django models

# Django rest framwork
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Reference models
from ..models import Reference

# Item models
from ..models import Item

# Item serializer
from ..serializers import ItemModelSerializer, AddItemSerializer

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    """ Item Viewset """

    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        """
            Inherited method to perform some actions needed before any request
            :param request: The resquest made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: The supermethod dispath object with the actions
        """
        reference_id = kwargs['reference']
        self.reference = get_object_or_404(
            Reference,
            id=reference_id
        )
        return super(ItemViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
            Creates the instance of the item
            :param request: the request object created from the request of the user
            :param args: Some arguments carried on the request
            :param kwargs: Some keyword arguments carried on the request
            :return: The serialized item created on the database
        """
        data = request.data.copy()
        data['reference'] = self.reference.id
        # Sends data to be validated
        serializer = AddItemSerializer(
            data=data,
            context={'request': request, 'stock': self.reference.stock}
        )
        # Validates data
        serializer.is_valid(raise_exception=True)
        # Saves object
        item = serializer.save()
        # Serializes object
        data = ItemModelSerializer(item).data
        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
            ** Terminar de validar **
            Deletes de detail of the selected item in the request url
            :param request: The request done by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some keyword arguments carried on the request
            :return: The response status
        """
        item = get_object_or_404(Item, id=kwargs['id'])
        order = item.order
        item.delete()
        if order.references.count() == 0:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)