from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import MeUserSerializer, UserSerializer
from .viewsets import RetrieveUpdateViewSet

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    search_fields = ('name',)


class MeUserViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer
