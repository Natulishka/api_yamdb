from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrSuperuser, IsAnyRole, IsModerator, IsUser
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, MeUserSerializer,
                          ReviewsSerializer, SignupSerializer,
                          TitlesSerializer, TokenSerializer, UserSerializer)
from .utils import email_confirmation_code
from .viewsets import CreateViewSet, RetrieveUpdateViewSet
from reviews.models import Categories, Comments, Genres, Reviews, Titles

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
        list_genre = []

        for obj_genre in self.request.data['genre']:
            list_genre.append(get_object_or_404(Genres, slug=obj_genre))
        serializer.save(
            genre=list_genre,
            category=get_object_or_404(
                Categories, slug=self.request.data['category']
            )
        )

    perform_update = perform_create


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
        serializer = self.get_serializer(data=request.data)
        try:
            username = request.data['username']
            email = request.data['email']
        except KeyError:
            serializer.is_valid(raise_exception=True)
        if not User.objects.filter(username=username,
                                   email=email).exists():
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.perform_create(serializer)
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        confirmation_code = default_token_generator.make_token(user)
        email_confirmation_code(confirmation_code, username, email)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)


class TokenViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def get_tokens_for_user(self, user):
        token = AccessToken.for_user(user)
        return {
            'token': str(token)
        }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response('Uncorrect value confirmation_code',
                            status=status.HTTP_400_BAD_REQUEST)
        token = self.get_tokens_for_user(user)
        return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    search_fields = ('name',)
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser)


class MeUserViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj
