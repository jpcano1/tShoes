""" User model """

#Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

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

    # Phone number regular expression to
    # check the number validation
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9, 20}$',
        message='Phone number must be entered in the format: +9999999999. Up to 20 digits allowed.'
    )

    # Phone number of the user
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_regex]
    )

    # The identity for the user of the platform
    identification = models.CharField(
        'Identification document',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "A user with that id already exists"
        }
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

    # Users profile picture
    profile_picture = models.ImageField(
        'Profile Image',
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    # User's bio
    biography = models.CharField(max_length=255, blank=True)

    # The resputation of the user, doesn't matters if it's customer, designer etc...
    reputation = models.FloatField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'identification']

    def __str__(self):
        """ String function """
        return "{} - email: {} - identification: {}".format(self.username, self.email, self.identification)

    def get_short_name(self):
        """ Returns username """
        return self.username