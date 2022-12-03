from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .serializers import SignupSerializer
from .utils import EmailConfirmationCode
# from .utils import generate_alphanum_crypt_string
from .viewsets import CreateViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.models import Categories, Comments, Genres, Reviews, Titles
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer
)


LEN_CONFIRMATION_CODE = 20
User = get_user_model()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category',)

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Categories, slug=self.request.data['category']
            )
        )

    def perform_update(self, serializer):
        return self.perform_create(self, serializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
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
            author=self.request.user,
            reviews=self.request_reviews()
        )


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        # confirmation_code = generate_alphanum_crypt_string(
        #     LEN_CONFIRMATION_CODE)
        confirmation_code = BaseUserManager().make_random_password(
            LEN_CONFIRMATION_CODE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        email = request.data['email']
        if User.objects.filter(username=username,
                               email=email).exists():
            instance = get_object_or_404(User, username=username)
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=True)
        serializer.save(password=confirmation_code)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        EmailConfirmationCode(confirmation_code, username, email)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)
