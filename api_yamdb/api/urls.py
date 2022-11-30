from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignupViewSet

api_v1_router = SimpleRouter()
# api_v1_router.register(
#     r'titles/(?P<title_id>[1-9]\d*)/reviews',
#     ReviewsViewSet,
#     basename='reviews'
# )
# api_v1_router.register(
#     r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments',
#     CommentsViewSet,
#     basename='comments'
# )


urlpatterns = [
    path('v1/auth/signup/', ),
    path('v1/', include(api_v1_router.urls), SignupViewSet),
]
