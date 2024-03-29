from datetime import date
from cobranca.models import Cobranca, Planilha
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MonthlyRecurringRevenueSerializer(serializers.Serializer):
    mrr = serializers.DecimalField(max_digits=10, decimal_places=2)

class StatisticsSerializer(serializers.Serializer):
    churm_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    mrr = serializers.DecimalField(max_digits=10, decimal_places=2)
    clientes_ativos = serializers.IntegerField()
    clientes_cancelados = serializers.IntegerField()

class UploadPlanilhaSerializer(serializers.Serializer):
    planilha = serializers.FileField()        


class CobrancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobranca
        fields = ('__all__')


class PlanilhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planilha
        fields = ('__all__')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nome'] = user.first_name
        token['sobrenome'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        groups = user.groups.all().values('id', 'name')
        token['group'] = [group for group in groups]
        print(token)
        return token

class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
