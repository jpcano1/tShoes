# Django Models
from django.db import models

# Designer
from users.models.designers import Designer

# Utils models
from utils.models import TShoesModel

class Inventory(TShoesModel, models.Model):
    """ Inventory Model """

    # The owner of the inventory
    designer = models.OneToOneField(Designer, on_delete=models.CASCADE, related_name='inventory')

    def __str__(self):
        """ String function """
        return "Inventory: {} - {}".format(str(self.id), str(self.designer))