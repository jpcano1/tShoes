# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

class Order(TShoesModel, models.Model):
    """
        Class that represents the order model
    """

    references = models.ManyToManyField('reference.Reference',
                                        through='reference.Item',
                                        through_fields=('order', 'reference'))
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, null=True)
    shipper = models.ForeignKey('users.Shipper', null=True, default=None, on_delete=models.SET_NULL)

