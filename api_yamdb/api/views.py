from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filtres import TitlesFilter
from .permissions import (IsAdminOrSuperuser, IsAdminOrSuperUserOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, MeUserSerializer,
                          ReviewsSerializer, SignupSerializer,
                          TitlesReadSerializer, TitlesWriteSerializer,
                          TokenSerializer, UserSerializer)
from .utils import send_email_confirmation_code
from .viewsets import CreateListDeleteViewSet, CreateViewSet
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
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
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
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
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
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
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        email = serializer.data['email']
        user, created = User.objects.get_or_create(
            username=username,
            email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_email_confirmation_code(confirmation_code, username, email)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
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
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
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

    def get_serializer_class(self):
        if self.action == 'me':
            return MeUserSerializer
        return UserSerializer

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        instance = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
