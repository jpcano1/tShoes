# Django Models
from django.db import models

# Designer
from users.models.designers import Designer

class Inventory(models.Model):
    """ Inventory Model """

    designer = models.OneToOneField(Designer, on_delete=models.CASCADE, related_name='Designer')

    def __str__(self):
        """ String function """
        return "Inventory: {} from designer: {}".format(str(self.pk), str(self.designer))