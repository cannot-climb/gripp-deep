from django.urls import path

from . import views


app_name = "kilterboard"

urlpatterns = [
    path("", views.IndexViewListView.as_view(), name="index"),
    path("upload", views.ClimbVideoCreateView.as_view(), name="upload"),
    path(
        "model/detect/hold/upload",
        views.HoldDetectionModelCreateView.as_view(),
        name="hold_detect_create",
    ),
]
