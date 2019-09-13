# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

class Order(TShoesModel, models.Model):
    """ Class that represents the order model
    """

