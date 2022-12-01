from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import ROLE_CHOICES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username',
                                            queryset=User.objects.all())
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
