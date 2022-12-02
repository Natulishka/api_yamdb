from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Categories, Comments, Genres, Reviews, Titles


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
