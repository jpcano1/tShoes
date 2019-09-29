# Django models
from django.db import models

# User Models
from users.models.users import User

class Customer(User, models.Model):
    """ Class that represents the customer
        Model from tShoes.
    """

    # Billing address of the user customer
    billing_adress = models.CharField(max_length=255, default=None)

    # City where the customer lives
    city = models.CharField(max_length=255, default=None)

    # Country where the customer lives
    country = models.CharField(max_length=255, default=None)

    # Zip code of the house of the
    zip_code = models.PositiveIntegerField(default=0)

    def __str__(self):
        """ toString function """
        return "Customer with name: {} and address: {}".format(self.first_name + " " + self.last_name,
                                                               str(self.billing_adress))