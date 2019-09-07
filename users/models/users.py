""" User model """

#Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from utils.models import TShoesModel

class User(AbstractUser, TShoesModel):
    """ User Model
     Extends from django's abstract base user
     """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'Auser with that email already exists'
        }
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user is verified'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """ String function """
        return "{} - email: {}".format(self.username, self.email)

    def get_short_name(self):
        """ Returns username """
        return self.username