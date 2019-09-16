# Django models
from django.db import models
# Utils models
from utils.models import TShoesModel

class Shipper(TShoesModel, models.Model):
    """ Class that represents the Shipper model """

    name = models.CharField(max_length=255, default=None)

    def __str__(self):
        """ toString function """
        return "The name of the enterprise: {}".format(self.name)