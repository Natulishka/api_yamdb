from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .serializers import SignupSerializer
from .utils import EmailConfirmationCode
# from .utils import generate_alphanum_crypt_string
from .viewsets import CreateViewSet

LEN_CONFIRMATION_CODE = 20
User = get_user_model()


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        # confirmation_code = generate_alphanum_crypt_string(
        #     LEN_CONFIRMATION_CODE)
        confirmation_code = BaseUserManager().make_random_password(
            LEN_CONFIRMATION_CODE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        email = request.data['email']
        if User.objects.filter(username=username,
                               email=email).exists():
            instance = get_object_or_404(User, username=username)
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=True)
        serializer.save(password=confirmation_code)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        EmailConfirmationCode(confirmation_code, username, email)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)
