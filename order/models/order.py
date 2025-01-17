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
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None,
                                 related_name='orders')

    # Shipper
    shipper = models.ForeignKey('users.Shipper',
                                null=True,
                                default=None,
                                on_delete=models.SET_NULL,
                                related_name='shipper_order')

    # optional address
    optional_address = models.CharField(max_length=255, default=None, null=True)

    NONE = 0
    PLACED = 1
    SHIPPED = 2
    ON_THE_WAY = 3
    ARRIVED = 4
    MISSING = 5

    STATUS_TYPE_CHOICES = ((NONE, 'none'),
                           (PLACED, 'placed'),
                           (SHIPPED, 'shipped'),
                           (ON_THE_WAY, 'on_the_way'),
                           (ARRIVED, 'arrived'),
                           (MISSING, 'missing'))

    # The actual status of the order
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPE_CHOICES, default=NONE)

    def __str__(self):
        """ toString function """
        return "Order {} with customer: {} and status: {}".format(str(self.id), self.customer.get_full_name(), self.status)