import os
import logging

from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ClimbVideo
from .serializer import ClimbVideoSerializer, ResponseClimbVideoSerializer
from . import customview

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
        status_code = model.save()

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
