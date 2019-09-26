""" User views """

# Django rest framework
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from users.models import User

# Serializers
from users.serializers import UserModelSerializer, UserSignUpSerializer

class UserViewset(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ user viewset
     handles Sign Up, login and account verification """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

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