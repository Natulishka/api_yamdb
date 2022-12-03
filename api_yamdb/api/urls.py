from api.views import MeUserViewSet, UserViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

api_v1_router = SimpleRouter()
api_v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/users/me/', MeUserViewSet.as_view({'get': 'retrieve',
                                                'path': 'update'})),
    path('v1/', include(api_v1_router.urls)),
]
