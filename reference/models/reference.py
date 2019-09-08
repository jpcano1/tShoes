# Django
from django.db import models

# Inventory models
from inventory.models import Inventory

class Reference(models.Model):
    """ Reference Model """

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='Inventory')