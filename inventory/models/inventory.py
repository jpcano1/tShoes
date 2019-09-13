# Django Models
from django.db import models

# Designer
from users.models.designers import Designer

# Utils models
from utils.models import TShoesModel

class Inventory(TShoesModel, models.Model):
    """ Inventory Model """

    designer = models.OneToOneField(Designer, on_delete=models.CASCADE, related_name='Designer')

    def __str__(self):
        """ String function """
        return "Inventory: {} from designer: {}".format(str(self.pk), str(self.designer))