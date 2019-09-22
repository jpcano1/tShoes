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

    # The email for each user in the plaform
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    # The identity for the user of the platform
    identification = models.CharField(
        'Identification document',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "A user with that id already exists"
        },
        primary_key=True
    )

    # Boolean that verifies the user is verified
    # in the platform
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user is verified'
    )

    # Boolean that verifies the user ID is verified
    # in the platform
    verified_id = models.BooleanField(
        'Verified Identification',
        default=False,
        help_text="Set to true when the user's ID is verified"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'identification']

    def __str__(self):
        """ String function """
        return "{} - email: {} - identification: {}".format(self.username, self.email, self.identification)

    def get_short_name(self):
        """ Returns username """
        return self.username