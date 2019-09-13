# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

# Order models
from order.models import Order

class Bill(TShoesModel, models.Model):
    """ Class that represents the bill of the order """

    order = models.OneToOneField(Order, on_delete=models.CASCADE)