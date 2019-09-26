""" User Serializer """

# Django models
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, password_validation
from django.conf import settings

# Django Rest Framework models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from users.models import User

# Serializers

# Utilities
from jose import jwt
from jose.jwt import *
from django.utils import timezone

class UserSignUpSerializer(serializers.Serializer):
    """ Class that allows us to create users and to send
        verification token to the user through the email.
    """

    # Email field
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Identification field
    identification = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Phone regular expression
    phone_regex = RegexValidator(
        regex=r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$',
        message='Invalid phone number format'
    )

    # phone number field
    phone_number = serializers.CharField(min_length=8, max_length=64)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Image
    profile_picture = serializers.ImageField(required=False, default=None)

    def validate(self, data):
        passwd = data['password']
        passwd_confirmation = data['password_confirmation']

        if passwd_confirmation != passwd:
            raise serializers.ValidationError("Passwords don't match")

        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user

    @staticmethod
    def gen_verificaion_token(user):
        """ Create JWT token that the user can use to verify its account """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

class UserModelSerializer(serializers.ModelSerializer):
    """ This class respresents the user model serializer """

    class Meta:
        """ Meta class """
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'identification',
                  )