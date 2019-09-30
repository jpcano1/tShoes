""" Item views """

# Django models

# Django rest framwork
from rest_framework import mixins, viewsets, status

# Order models
from order.models import Order

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin):
    """ Item Viewset """

