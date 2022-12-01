from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignupViewSet

api_v1_router = SimpleRouter()

urlpatterns = [
    path('v1/auth/signup/', SignupViewSet.as_view()),
    path('v1/', include(api_v1_router.urls)),
]
