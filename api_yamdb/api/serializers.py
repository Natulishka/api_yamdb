import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'confirmation_code')
        model = User
        read_only_fields = ('confirmation_code',)

    def validate_username(self, value):
        username = self.context['request'].username
        if username == 'me':
            raise serializers.ValidationError('Нельзя использовать в качестве'
                                              ' username строку me!')
        if not re.fullmatch(r'[\w.@+-]+', username):
            raise serializers.ValidationError('username может содержать только'
                                              ' цифры, буквы или символы .@+-')
        return value
