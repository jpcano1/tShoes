# Django
from django.db import models

# Inventory models
from inventory.models import Inventory

class Reference(models.Model):
    """ Reference Model """

    reference = models.CharField(max_length=255, default=None)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='Inventory')

    def __str__(self):
        """ String function """
        return "Reference: {} from inventory: {}".format(self.reference, str(self.inventory))
