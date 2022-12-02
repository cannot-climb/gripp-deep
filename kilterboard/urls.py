from django.urls import path

from . import views


app_name = "kilterboard"

urlpatterns = [
    path("", views.IndexViewListView.as_view(), name="index"),
    path("upload", views.ClimbVideoCreateView.as_view(), name="upload"),
]
