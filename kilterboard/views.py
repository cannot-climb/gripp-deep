from rest_framework import generics, status
from rest_framework.response import Response

from .models import ClimbVideo
from .serializer import ClimbVideoSerializer


class IndexViewListView(generics.ListAPIView):
    queryset = ClimbVideo.objects.all()
    serializer_class = ClimbVideoSerializer


class ClimbVideoCreateView(generics.CreateAPIView):
    serializer_class = ClimbVideoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # video: ClimbVideo = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # print(video.video.path)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()
