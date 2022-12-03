from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignupViewSet
from api.views import CommentsViewSet, ReviewsViewSet, CategoriesViewSet, GenresViewSet, TitlesViewSet

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
    path('v1/', include(api_v1_router.urls)),
]
