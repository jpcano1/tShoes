""" Designers permissions """

# Django rest framework
from rest_framework.permissions import BasePermission

# Models
from ..models import Designer

from inventory.models import Inventory

class IsDesigner(BasePermission):
    """ Class that represents the validations of the designer """

    def has_permission(self, request, view):
        try:
            Designer.objects.get(id=request.user.id)
            if request.user.is_verified:
                return True
            else:
                return False
        except Designer.DoesNotExist:
            return False

class IsInventoryOwner(BasePermission):
    """ Class that validates the requesting user is the owner of the inventory """

    def has_permission(self, request, view):
        inventory = view.kwargs.get('inventory')
        try:
            Inventory.objects.get(id=inventory, designer=request.user.id)
            return True
        except Inventory.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.designer.id:
            return True
        return False

class IsReferenceOwner(BasePermission):
    """  """
    def has_object_permission(self, request, view, obj):
        """

            :param request:
            :param view:
            :param obj:
            :return:
        """
        if request.user.id == obj.inventory.designer.id:
            return True
        return False