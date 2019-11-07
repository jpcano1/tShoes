""" Customer views """

# Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

# Customer models
from ..models import Customer

# Order models
from order.models import Order

# Item models
from reference.models import Item

# Customer Serializers
from ..serializers import CustomerModelSerializer, CustomerSignUpSerializer

# Order serializer
from order.serializers import OrderModelSerializer

# Item serializers
from reference.serializers import ItemModelSerializer

# Bill Serializers
from bill.serializers import CreateBillSerializer, BillModelSerializer

# Permissions
from ..permissions import (IsCustomer,
                           IsOrderOwner,
                           IsItemOwner,
                           IsAccountOwner,
                           IsVerified)
from rest_framework.permissions import IsAuthenticated, AllowAny

class CustomerViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    """ Customer viewset, here is where the CRUD of the customer is developed """
    queryset = Customer.objects.all()
    serializer_class = CustomerModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = []
        if self.action in ['create']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permissions = [IsAccountOwner,
                           IsVerified,
                           IsAuthenticated]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """ Documentar """
        serializer = CustomerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        data = CustomerModelSerializer(customer).data
        return Response(data, status=status.HTTP_201_CREATED)

class CustomerOrderViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin):
    """ Customer - Order viewset """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """
             Definir permisos para lista y para compra
            :return: El permiso asociado a la petición respectiva.
        """
        permissions = [IsCustomer, IsAuthenticated, IsVerified]
        if self.action in ['retrieve',
                           'update',
                           'partial_update',
                           'destroy',
                           'place']:
            permissions.append(IsOrderOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        customer_id = kwargs['customer']
        self.customer = get_object_or_404(Customer, id=customer_id)
        return super(CustomerOrderViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            Retrieves the list of customers
            :param request: the request object
            :param args: the arguments of the request
            :param kwargs: the keyword arguments
            :return: The list of customers
        """
        customer = self.customer
        orders = Order.objects.filter(customer=customer)
        data = OrderModelSerializer(orders, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        customer = self.customer
        order = get_object_or_404(Order, customer=customer, id=kwargs['id'])
        if order.status == 0:
            order.delete()
        else:
            return Response("You can't delete this order", status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def place(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['id'], customer=self.customer)
        serializer = CreateBillSerializer(data={'order': order.id})
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        data = BillModelSerializer(bill).data
        return Response(data, status=status.HTTP_201_CREATED)

class CustomerItemViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """ Customer - Item Viewset """

    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """ Definir permisos para lista """
        permissions = [IsAuthenticated, IsCustomer, IsVerified]
        if self.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            permissions.append(IsItemOwner)
        return [p() for p in permissions]


    def dispatch(self, request, *args, **kwargs):
        customer_id = kwargs['customer']
        order_id = kwargs['order']
        self.customer = get_object_or_404(Customer, id=customer_id)
        self.order = get_object_or_404(Order, customer=customer_id, id=order_id)
        return super(CustomerItemViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        items = Item.objects.filter(order=self.order)
        data = ItemModelSerializer(items, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs['id'])
        partial = request.method == 'PATCH'
        serializer = ItemModelSerializer(item, data=request.data, context={
            'reference': item.reference,
            'item': item
        }, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ItemModelSerializer(item).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs['id'])
        order = item.order
        item.delete()
        if order.references.count() == 0:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)