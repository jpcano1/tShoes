"""  """

# Models
from ..models import Customer

from order.models import Order

# Django rest framework
from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """  """

    def has_permission(self, request, view):
        """

            :param request:
            :param view:
            :return:
        """
        try:
            Customer.objects.get(id=request.user.id)
            if request.user.is_verified:
                return True
            else:
                return False
        except Customer.DoesNotExist:
            return False

class IsOrderOwner(BasePermission):
    """ This class allows me to verify the requesting user is the owner of
     the order """

    def has_permission(self, request, view):
        try:
            order_id = view.kwargs.get('id')
            user_id = view.kwargs.get('customer')
            Order.objects.get(id=order_id, customer=user_id)
            return True
        except Order.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """
            Verifies the access over the object requested
            :param request: The object request
            :param view: The view from which the request is comming
            :param obj: The requested object
            :return: A boolean that determines
            whether the user is allowed or not
        """
        if obj.customer.id == request.user.id:
            return True
        return False

class IsItemOwner(BasePermission):
    """ This class allows me to verify the requesting user is the owner of
     the items in the order """

    def has_object_permission(self, request, view, obj):
        """
            Verifies the access over the object requested
            :param request: The object request
            :param view: The view from which the request is comming
            :param obj: The requested object
            :return: A boolean that determines
            whether the user is allowed or not
        """
        if obj.order.customer.id == request.user.id:
            return True
        return False