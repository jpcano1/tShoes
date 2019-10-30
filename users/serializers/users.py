""" User Serializer """

# Django models
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, password_validation
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Django Rest Framework models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication

# Models
from users.models import User

# Serializers

# Utilities
from jose import jwt
from jose import *
from django.utils import timezone
from datetime import timedelta

# Nexmo Messages
from nexmo import *

# Auth0 Dependencies
from auth0.v2 import authentication
from auth0.v2.authentication import base

import requests

class BearerAuth(TokenAuthentication):
    keyword = 'Bearer'

class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification Serializer that allows to know which user has a
    verificated account and which doesn't
    """

    token = serializers.CharField()

    def validate(self, data):
        """ Validate method for the token """
        try:
            payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise serializers.ValidationError("The token has expired.")
        except JWTError:
            raise serializers.ValidationError("Error validating token. Ensure is the right token.")

        self.context['payload'] = payload
        return data

    def save(self, **kwargs):
        """ Update the user's verification status """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()


class LoginSerializer(serializers.Serializer, ):
    """ Login serializer to make a login to a User """

    password_less = authentication.Passwordless(settings.SOCIAL_AUTH_AUTH0_DOMAIN)
    context = {}

    code = serializers.CharField()

    @staticmethod
    def start(data):
        try:
            User.objects.get(email=data['email'])
            response = LoginSerializer.password_less.email(client_id=settings.SOCIAL_AUTH_AUTH0_KEY,
                                                email=data['email'],
                                                send='code')
            if response.get('email_verified'):
                raise serializers.ValidationError("You are not verified, you cannot login")
            LoginSerializer.context['email'] = response['email']
            return "You can go check your email to obtain the authorization code"
        except User.DoesNotExist:
            raise PermissionDenied("The user doesn't exist on our database")

    def validate(self, data):
        """ Function that makes the validation email-password """
        print(data)
        print(self.context)
        auth_data = {
            "client_id": settings.SOCIAL_AUTH_AUTH0_KEY,
            "connection": "email",
            "email": LoginSerializer.context.get('email'),
            "verification_code": data['code']
        }
        # auth_data["email"] = self.context.get('email')
        # auth_data['client_id'] = settings.SOCIAL_AUTH_AUTH0_KEY
        # auth_data['connection'] = "email"
        response = requests.post(url="https://" + settings.SOCIAL_AUTH_AUTH0_DOMAIN + "/passwordless/verify", data=auth_data)

        if response.text != 'OK':
            raise serializers.ValidationError(response.json()["error_description"])

        user = User.objects.get(email=LoginSerializer.context.get('email'))

        if user.is_verified:
            raise PermissionDenied("The user is not verified, please check your email")

        self.context['user'] = user
        return data

    def create(self, data):
        """ Get or create token """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):
    """ Class that allows us to create users and to send
        verification token to the user through the email.
    """
    database = authentication.Database(domain=settings.SOCIAL_AUTH_AUTH0_DOMAIN)

     # Username of the user
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

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
    phone_number = serializers.CharField(validators=[phone_regex], required=True)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # First_name and last_name of the username
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Image of the user
    profile_picture = serializers.ImageField(required=False, default=None)

    def validate(self, data):
        print(data)
        passwd = data['password']
        passwd_confirmation = data['password_confirmation']

        if passwd_confirmation != passwd:
            raise serializers.ValidationError("Passwords don't match")

        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        """

        :param data:
        :return:
        """
        data.pop('password_confirmation')
        self.database.signup(client_id=settings.SOCIAL_AUTH_AUTH0_KEY,
                             email=data['email'],
                             password=data['password'],
                             connection=settings.AUTH0_DATABASE_CONNECTION)
        user = User.objects.create_user(**data)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """ Send account verification link to given user """
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user
            })
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach(content, 'text/html')
        msg.send()
        print("Sending email")

    def gen_verification_token(self, user):
        """ create JWT token that the user can use to verify its account. """
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
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'identification',]