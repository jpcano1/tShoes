"""  """

# Models
from ..models import Customer

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
    """  """

    def has_object_permission(self, request, view, obj):
        """

            :param request:
            :param view:
            :param obj:
            :return:
        """
        if obj.customer.id == request.user.id:
            return True
        return False

class IsItemOwner(BasePermission):
    """  """

    def has_object_permission(self, request, view, obj):
        """

            :param request:
            :param view:
            :param obj:
            :return:
        """
        if obj.order.customer.id == request.user.id:
            return True
        return False