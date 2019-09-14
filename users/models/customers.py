# Django models
from django.db import models

# User Models
from users.models.users import User

class Customer(User, models.Model):
    """ Class that represents the customer
        Model from tShoes.
    """
