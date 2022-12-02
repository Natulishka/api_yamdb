import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать в качестве'
                                              ' username строку me!')
        if not re.fullmatch(r'[\w.@+-]+', value):
            raise serializers.ValidationError('username может содержать только'
                                              ' цифры, буквы или символы .@+-')
        return value
