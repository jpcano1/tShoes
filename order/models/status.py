""" Status model """

# Django models
from django.db import models

class Status(models.Model):
    """  """
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

    id = models.PositiveSmallIntegerField(choices=STATUS_TYPE_CHOICES, primary_key=True)

    def __str__(self):
        """ toString function """
        return self.get_id_display()