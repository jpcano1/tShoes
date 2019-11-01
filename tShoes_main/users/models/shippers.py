# Django models
from django.db import models
# Utils models
from users.models import User

class Shipper(User, models.Model):
    """ Class that represents the Shipper model """

    def __str__(self):
        """ toString function """
        return "The name of the enterprise: {}".format(self.first_name)