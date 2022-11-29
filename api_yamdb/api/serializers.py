from rest_framework import serializers

from reviews.models import Reviews, Comments


class ReviewsSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ('titles', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('titles',)

    # def get_score(self, obj):
    #     obj_score = []

    #     for obj_model in Reviews.objects.filter(author=1):
    #         obj_score.append(obj_model.score)

    #     return sum(obj_score) // len(obj_score)


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('reviews',)
