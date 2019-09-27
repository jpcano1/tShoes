# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

class Bill(TShoesModel, models.Model):
    """ Class that represents the bill of the order """

    # The order that owns the bill
    order = models.OneToOneField('order.Order', on_delete=models.CASCADE)

    # Total price of the
    total_price = models.FloatField(default=0)

    def __str__(self):
        """ toString function """
        return "id of the bill: {} and the total price: {}".format(str(self.pk), str(self.total_price))