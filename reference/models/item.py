# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

# Reference models
from reference.models import Reference

# Order models
from order.models import Order

class Item(TShoesModel, models.Model):
    """ Class that represents the Item models
        This is an intermediate relationship for
        the one-to-many relation between Order and
        Reference.
     """

    # attribute that models the quantity of a reference
    # inside an order
    quantity = models.PositiveIntegerField()

    # Atribute that models the reference of the shoe
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    # Attibute that models the order of shoes
    order = models.ForeignKey(Order, on_delete=models.CASCADE)