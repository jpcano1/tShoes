# Django models
from django.db import models

# Inventory models
from inventory.models import Inventory

# Utils models
from utils.models import TShoesModel

class Reference(TShoesModel, models.Model):
    """ Reference Model """

    # Name of the reference
    reference_name = models.CharField(max_length=255, default=None)

    # Description of the reference
    description = models.CharField(max_length=255, default=None, blank=True, null=True)

    # Price of the reference
    price = models.FloatField(blank=True, default=None)

    # The inventory that owns this reference
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='references')

    # The image of the reference
    reference_image = models.ImageField(
        "Image of the reference to buy",
        upload_to="inventory/references/",
        blank=True,
        null=True
    )

    # The min stock for sale
    min_stock = models.PositiveIntegerField(default=0)

    # The max stock for sale
    max_stock = models.PositiveIntegerField(default=None)

    # The number of occurences of this reference
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        """ String function """
        return "Reference: {} from inventory: {}".format(self.reference_name, str(self.inventory))