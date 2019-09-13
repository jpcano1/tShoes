# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

# Reference models
from .reference import Reference

# Order models
from order.models import Order

class Item(TShoesModel, models.Model):
    """ Class that represents the Item models
        This is an intermediate relationship for
        the one-to-many relation between Oeder and
        Reference.
     """

    quantity = models.PositiveIntegerField()
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)