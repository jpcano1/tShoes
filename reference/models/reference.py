# Django
from django.db import models

# Inventory models
from inventory.models import Inventory

# Utils models
from utils.models import TShoesModel

class Reference(TShoesModel, models.Model):
    """ Reference Model """

    #
    reference_name = models.CharField(max_length=255, default=None)

    #
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='Inventory')

    #
    min_stock = models.PositiveIntegerField()

    #
    max_stock = models.PositiveIntegerField()

    def __str__(self):
        """ String function """
        return "Reference: {} from inventory: {}".format(self.reference_name, str(self.inventory))