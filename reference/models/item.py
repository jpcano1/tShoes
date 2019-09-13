# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

class Item(TShoesModel, models.Model):
    """ Class that represents the Item models
        This is an intermediate relationship for
        the one-to-many relation between Oeder and
        Reference.
     """

    quantity = models.PositiveIntegerField()