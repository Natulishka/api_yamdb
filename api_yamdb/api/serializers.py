import re

# from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import get_user_model
# from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.settings import api_settings
from reviews.models import Categories, Comments, Genres, Reviews, Titles

# from rest_framework.validators import UniqueTogetherValidator


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

    def get_rating(self, obj):
        try:
            obj_score = []

            for obj_model in Reviews.objects.filter(titles=obj.id):
                obj_score.append(obj_model.score)

            return sum(obj_score) // len(obj_score)
        except Exception:
            return 0


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('titles',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Reviews.objects.all(),
        #         fields=('titles', 'author'),
        #         message='Вы уже оставляли отзыв на это произведение!'
        #     )
        # ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('reviews',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    password = serializers.HiddenField(default=1)

    class Meta:
        model = User
        fields = ('user', 'password', 'confirmation_code')

    # confirmation_code = serializers.CharField(source='password')

#     # def __init__(self, *args, **kwargs):
#     #     # Вызываем конструктор класса-родителя.
#     #     print("проверка2")
#     #     print(self.__dict__)
#     #     super().__init__(self, *args, **kwargs)
#     #     # Передаём значение параметра в новое свойство.

#     # def validate(self, attrs):
#     #     print("проверка3")
#     #     authenticate_kwargs = {
#     #         self.username_field: attrs[self.username_field],
#     #         "confirmation_code": attrs["confirmation_code"],
#     #     }
#     #     try:
#     #         authenticate_kwargs["request"] = self.context["request"]
#     #     except KeyError:
#     #         pass

#     #     self.user = authenticate(**authenticate_kwargs)

#     #     if not api_settings.USER_AUTHENTICATION_RULE(self.user):
#     #         raise exceptions.AuthenticationFailed(
#     #             self.error_messages["no_active_account"],
#     #             "no_active_account",
#     #         )

#     #     return {}
