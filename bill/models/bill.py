# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

class Bill(TShoesModel, models.Model):
    """ Class that represents the bill of the order """

    order = models.OneToOneField('order.Order', on_delete=models.CASCADE)