""" User views """

# Django rest framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from users.models import User

# Serializers
from users.serializers import (UserModelSerializer,
                               UserSignUpSerializer,
                               UserLoginSerializer)

class UserViewset(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ user viewset
     handles Sign Up, login and account verification """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        """ add extra data to the response """
        response = super(UserViewset, self).retrieve(request, *args, **kwargs)
        data = {
            'user': response.data
        }
        response.data = data
        return response

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """ User sign up """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """ User sign up """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)