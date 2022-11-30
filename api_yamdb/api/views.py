from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from .serializers import SignupSerializer
from .utils import EmailConfirmationCode, generate_alphanum_crypt_string
from .viewsets import CreateViewSet

LEN_CONFIRMATION_CODE = 10
User = get_user_model()


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        confirmation_code = generate_alphanum_crypt_string(
            LEN_CONFIRMATION_CODE)
        username = request.data['username']
        email = request.data['email']
        if not User.objects.filter(username=username,
                                   email=email).exists():
            serializer = self.get_serializer(data=request.data)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=confirmation_code)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        EmailConfirmationCode(confirmation_code, username, email)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)
