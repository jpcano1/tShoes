# Django models
from django.db import models

# Utils models
from utils.models import TShoesModel

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
                                 on_delete=models.CASCADE,
                                 null=True)

    # Shipper
    shipper = models.ForeignKey('users.Shipper',
                                null=True,
                                default=None,
                                on_delete=models.SET_NULL)

    # Designer
    designer = models.ForeignKey('users.Designer',
                                 on_delete=models.CASCADE,
                                 null=True)

    # optional address
    optional_adress = models.CharField(max_length=255, default=None)