from rest_framework import views, status
from rest_framework.response import Response

from accounts.serializer import UserLoginSerializer


class TokenObtainPairView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT
            )

        response_data = {
            "access": serializer.data["access_token"],
            "refresh": serializer.data["refresh_token"],
        }

        if serializer.validated_data["username"] == "None":
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        return Response(response_data, status=status.HTTP_200_OK)
