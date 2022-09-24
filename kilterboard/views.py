from rest_framework import generics, status
from rest_framework.response import Response

from .models import ClimbVideo
from .serializer import ClimbVideoSerializer


class IndexViewListView(generics.ListAPIView):
    queryset = ClimbVideo.objects.all()
    serializer_class = ClimbVideoSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {"message": "token is needed"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return super().get(request, *args, **kwargs)


class ClimbVideoCreateView(generics.CreateAPIView):
    serializer_class = ClimbVideoSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {"message": "token is needed"}, status=status.HTTP_401_UNAUTHORIZED
            )
