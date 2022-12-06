from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filtres import TitlesFilter
from .permissions import (IsAdminOrSuperuser,
                          IsAdminOrSuperuserWithSafeMethods,
                          ReviewsAndCommentsPermissions)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, MeUserSerializer,
                          ReviewsSerializer, SignupSerializer,
                          TitlesReadSerializer, TitlesWriteSerializer,
                          TokenSerializer, UserSerializer)
from .utils import email_confirmation_code
from .viewsets import (CreateListDeleteViewSet, CreateViewSet,
                       RetrieveUpdateViewSet)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrSuperuserWithSafeMethods,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrSuperuserWithSafeMethods,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrSuperuserWithSafeMethods,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = (TitlesFilter)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (ReviewsAndCommentsPermissions,)
    ordering = ('-id',)

    def request_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.request_title().reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
            title=self.request_title(),
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
    permission_classes = (ReviewsAndCommentsPermissions,)
    ordering = ('-id',)

    def request_reviews(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.request_reviews().comments.all()

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
    permission_classes = (IsAdminOrSuperuser, )
    ordering = ('username',)


class MeUserViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj
