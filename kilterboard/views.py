import datetime
import os
import uuid
from urllib import request
from urllib.parse import urlparse

from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ClimbVideo
from .serializer import ClimbVideoSerializer, ResponseClimbVideoSerializer
from . import customview


class IndexViewListView(generics.ListAPIView):
    queryset = ClimbVideo.objects.all()
    serializer_class = ClimbVideoSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {"message": "token is needed"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return super().get(request, *args, **kwargs)


class ClimbVideoCreateView(customview.GenericAPIView, customview.CreateModelMixin):
    serializer_class = ClimbVideoSerializer
    response_serializer_class = ResponseClimbVideoSerializer

    def post(self, request, *args, **kwargs):
        model = self.create(request, *args, **kwargs)
        self.set_model(model)

        serializer = self.create_response(model)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def set_model(self, model):
        video_url = model.video_url
        base_name = self.get_unique_basename(urlparse(video_url).path)
        video_path = os.path.join(settings.MEDIA_ROOT, base_name)
        request.urlretrieve(video_url, video_path)

        model.video = base_name
        model.start_time = datetime.time(minute=10, second=10)
        model.end_time = datetime.time(minute=20, second=10)
        model.success = True

        model.save()

    def get_unique_basename(self, path):
        base_name = os.path.basename(path)
        filename, extension = os.path.splitext(base_name)
        return filename + "-" + str(uuid.uuid4()).replace("-", "") + extension
