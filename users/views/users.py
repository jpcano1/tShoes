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
                               LoginSerializer,
                               AccountVerificationSerializer)

class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ user viewset
     handles Sign Up, login and account verification """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """ add extra data to the response """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = UserModelSerializer(response.data).data
        response.data = data
        return response

    def list(self, request, *args, **kwargs):
        """ The list mixin view """
        response = super(UserViewSet, self).list(request, *args, **kwargs)
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
        """ Creates an user in the database with is_verified value = False """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """

            :param request:
            :return:
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)