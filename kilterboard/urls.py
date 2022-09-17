from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexViewListView.as_view(), name="index"),
    path("upload", views.ClimbVideoCreateView.as_view(), name="upload"),
]
