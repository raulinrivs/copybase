from artigos.models import Artigo
from rest_framework import serializers


class ArtigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artigo
        fields = ('__all__')
