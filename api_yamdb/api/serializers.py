from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comments, Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('titles',)
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('titles', 'author'),
                message='Вы уже оставляли отзыв на это произведение!'
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('reviews',)
