from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (IsAdminOrSuperuser, IsAuthor, IsModerator,
                          IsSafeMethods, IsUser)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, MeUserSerializer,
                          ReviewsSerializer, SignupSerializer,
                          TitlesSerializer, TokenSerializer, UserSerializer)
from .utils import email_confirmation_code
from .viewsets import (CreateListDeleteViewSet, CreateViewSet,
                       RetrieveUpdateViewSet)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (
        IsSafeMethods | (IsAuthenticated & IsAdminOrSuperuser),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (
        IsSafeMethods | (IsAuthenticated & IsAdminOrSuperuser),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (
        IsSafeMethods | (IsAuthenticated & IsAdminOrSuperuser),
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',)

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        if genre is not None:
            genres = get_object_or_404(Genre, slug=genre)
            queryset = genres.titles.all()
        if category is not None:
            categories = get_object_or_404(Category, slug=category)
            queryset = categories.titles.all()
        return queryset

    def perform_create(self, serializer):
        list_genre = []

        for obj_genre in self.request.data.getlist('genre'):
            list_genre.append(get_object_or_404(Genre, slug=obj_genre))

        serializer.save(
            genre=list_genre,
            category=get_object_or_404(
                Category, slug=self.request.data['category']
            )
        )

    perform_update = perform_create


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (
        IsSafeMethods | (IsAuthenticated & (
            IsAuthor | IsAdminOrSuperuser | IsModerator)),)

    def perform_create(self, serializer):
        if Review.objects.filter(
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id')),
            author=self.request.user
        ).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв')

        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsSafeMethods | (
        IsUser | IsAdminOrSuperuser | IsModerator),)

    def request_reviews(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
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
