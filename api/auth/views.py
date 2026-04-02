from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.serializers import AuthUserSerializer


class AuthUserView(APIView):
    def get(self, request):
        serializer = AuthUserSerializer(request.user)
        return Response(serializer.data)
