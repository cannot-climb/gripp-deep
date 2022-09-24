from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("token/obtain", views.TokenObtainPairView.as_view(), name="obtain_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
]
