from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import MeUserViewSet, UserViewSet

api_v1_router = SimpleRouter()
api_v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/users/me/', MeUserViewSet.as_view({'get': 'retrieve',
                                                'path': 'update'})),
    path('v1/', include(api_v1_router.urls)),
]
