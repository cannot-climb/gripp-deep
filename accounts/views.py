from rest_framework import views, status
from rest_framework.response import Response

from accounts.serializer import UserLoginSerializer


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT
            )

        response_data = {"token": serializer.data["access_token"]}
        return Response(response_data, status=status.HTTP_200_OK)
