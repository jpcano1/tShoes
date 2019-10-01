# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

from .status import Status

class Order(TShoesModel, models.Model):
    """
        Class that represents the order model
    """

    # References contained in the order
    references = models.ManyToManyField('reference.Reference',
                                        through='reference.Item',
                                        through_fields=('order', 'reference'))

    # Customer
    customer = models.ForeignKey('users.Customer',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None,
                                 related_name='order')

    # Shipper
    shipper = models.ForeignKey('users.Shipper',
                                null=True,
                                default=None,
                                on_delete=models.SET_NULL,
                                related_name='shipper_order')

    # optional address
    optional_address = models.CharField(max_length=255, default=None, null=True)

    # The actual status of the order
    # status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)