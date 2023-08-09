from artigos.models import Artigo
from artigos.serializers import ArtigoSerializer
from artigos.utils import news_api_request

from rest_framework.response import Response
from rest_framework import permissions, views, status


class ArtigoAPIView(views.APIView):
    serializer_class = ArtigoSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = news_api_request()
        serializer = self.serializer_class(data=data['articles'], many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_200_OK, data=serializer.data)
