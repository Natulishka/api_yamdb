from api.views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                       ReviewsViewSet, TitlesViewSet)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignupViewSet, TokenViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView


app_name = 'api'

api_v1_router = SimpleRouter()
api_v1_router.register('titles', TitlesViewSet)
api_v1_router.register('categories', CategoriesViewSet)
api_v1_router.register('genres', GenresViewSet)
api_v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
api_v1_router.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments',
    CommentsViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', SignupViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/', TokenViewSet.as_view({'post': 'create'}),
         name='token_obtain_pair'),
    path('v1/', include(api_v1_router.urls)),
]
