from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import ReviewsSerializer, CommentsSerializer
from reviews.models import Reviews, Comments


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(
            titles=get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        )


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def request_reviews(self):
        return get_object_or_404(
            Reviews,
            titles=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.request_reviews().comments

    def perform_create(self, serializer):
        serializer.save(
            reviews=self.request_reviews()
        )
