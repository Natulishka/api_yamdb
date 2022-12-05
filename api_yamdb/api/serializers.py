from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles
from users.models import ROLE_CHOICES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class MeUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role', )


class SignupSerializer(serializers.ModelSerializer):

    # username = serializers.RegexField(regex=r'^[\w.@+-]+$')

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать в качестве'
                                              ' username строку me!')
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
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug',)
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
            return None

    def validate_year(self, value):
        if len(str(value)) != 4:
            raise serializers.ValidationError('Неверный формат года!')

        if not (datetime.today().year >= value):
            raise serializers.ValidationError('Неверно указан год!')

        return value


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('titles',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('reviews',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
