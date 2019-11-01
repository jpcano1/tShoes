""" User views """

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as log_out

# Json
import json

# Urllib
from urllib.parse import urlencode

# Django rest framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
# Models
from ..models import User
# Serializers
from ..serializers import (UserModelSerializer,
                               UserSignUpSerializer,
                               LoginSerializer,
                               AccountVerificationSerializer)
from ..permissions import (IsAccountOwner, )

def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'auth/index.html')

def email_verified(request):
    return render(request, 'auth/verification.html')

@login_required
def dashboard(request):
    print(request.user)
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    return render(request, 'auth/dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })

def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    """ user viewset
     handles Sign Up, login and account verification """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = []
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        if self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAccountOwner]
        return [p() for p in permissions]

    def retrieve(self, request, *args, **kwargs):
        """ add extra data to the response """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = UserModelSerializer(response.data).data
        response.data = data
        return response

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """ Verifies an profile through token validation """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"Message": "Congratulations, now go check the page!!!"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
            Creates an user in the database with
            is_verified value = False
            :param request:
            :return:
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
            Login Method passwordless
            :param request: The request done by the user
            :return: The response of the request
        """
        serializer = LoginSerializer.start(data=request.data)
        return Response(serializer, status=status.HTTP_201_CREATED)

    # @action(detail=False, methods=['post'])
    # def code_verify(self, request):
    #     """
    #         Verifies the email and the auth code are correct
    #         :param request:
    #         :return:
    #     """
    #     serializer = LoginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user, token = serializer.save()
    #     data = {
    #         "user": UserModelSerializer(user).data,
    #         "access_token": token
    #     }
    #     return Response(data, status=status.HTTP_200_OK)