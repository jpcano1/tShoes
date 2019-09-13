# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

# Reference models
from reference.models import Reference

class Order(TShoesModel, models.Model):
    """ Class that represents the order model
    """

    reference = models.ManyToManyField(Reference, through='Item')
