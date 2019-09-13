# Django
from django.db import models

# Inventory models
from inventory.models import Inventory

#Order models
from order.models import Order

# Item models
from .item import Item

class Reference(models.Model):
    """ Reference Model """

    reference = models.CharField(max_length=255, default=None)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='Inventory')
    order = models.ManyToManyField(Order, through='Item')

    def __str__(self):
        """ String function """
        return "Reference: {} from inventory: {}".format(self.reference, str(self.inventory))
