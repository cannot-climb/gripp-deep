import datetime
import os
import uuid
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlparse
import logging

from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ClimbVideo
from .serializer import ClimbVideoSerializer, ResponseClimbVideoSerializer
from . import customview
from .cv import get_hold_mask, get_video_result

logger = logging.getLogger("gripp.settings")


class IndexViewListView(generics.ListAPIView):
    queryset = ClimbVideo.objects.all()
    serializer_class = ResponseClimbVideoSerializer

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
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        if request.user.is_anonymous:
            return Response(
                {"message": "token is needed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        model = self.create(request, *args, **kwargs)
        status_code = self.set_model(model)

        if status_code == 404:
            return Response(
                {"message": "videoUrl is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        if status_code == 401:
            logger.error("os.environ['GRIPP_BASIC_TOKEN'] is not valid")
            return Response(
                {"message": "server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = self.create_response(model)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def set_model(self, model: ClimbVideo) -> int:
        video_url = model.video_url
        base_name = self.get_unique_basename(urlparse(video_url).path)
        video_path = os.path.join(settings.MEDIA_ROOT, base_name)

        try:
            opener = request.build_opener()
            opener.addheaders = [
                ("Authorization", f"Basic {os.environ['GRIPP_BASIC_TOKEN']}")
            ]
            request.install_opener(opener)
        except KeyError:
            logger.error("os.environ['GRIPP_BASIC_TOKEN'] does not found")

        try:
            request.urlretrieve(video_url, video_path)
        except HTTPError as e:
            return e.status

        hand_hold_mask, start_hold_mask, top_hold_mask = get_hold_mask(video_path)
        start_second, end_second, success = get_video_result(
            video_path, hand_hold_mask, start_hold_mask, top_hold_mask
        )

        start_second_int = int(start_second)
        end_second_int = int(end_second)

        model.video = base_name
        model.start_time = datetime.time(
            start_second_int // 3600,
            (start_second_int % 3600) // 60,
            start_second_int % 60,
            int((start_second - start_second_int) * 1000),
        )
        model.end_time = datetime.time(
            end_second_int // 3600,
            (end_second_int % 3600) // 60,
            end_second_int % 60,
            int((end_second - end_second_int) * 1000),
        )
        model.success = success

        model.save()

        return 200

    def get_unique_basename(self, path):
        base_name = os.path.basename(path)
        filename, extension = os.path.splitext(base_name)
        return filename + "-" + str(uuid.uuid4()).replace("-", "") + extension
