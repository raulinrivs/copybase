from cobranca.models import Cobranca, Planilha
from cobranca.serializers import CobrancaSerializer, PlanilhaSerializer, StatisticsSerializer, TokenBlacklistResponseSerializer, \
    TokenRefreshResponseSerializer, TokenVerifyResponseSerializer, MyTokenObtainPairSerializer, \
    UploadPlanilhaSerializer
from rest_framework import viewsets, status, permissions, filters, generics
from rest_framework.response import Response
from openpyxl import load_workbook
from datetime import date, datetime
import pandas as pd
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class StatisticsAPIView(generics.GenericAPIView):
    queryset = Cobranca.objects.all()
    serializer_class = StatisticsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['data_inicio', ]

    def get(self, request):
        serializer = self.get_serializer
        params = self.request.query_params
        datetime_inicio = datetime.fromisoformat(params.get('data_inicio'))
        base_queryset = self.queryset.filter(
            data_inicio__year = datetime_inicio.year,
            data_inicio__month = datetime_inicio.month,
            planilha__id = params.get('id')
        )

        clientes_ativos = self.queryset.filter(
            status='Ativa',
            planilha__id = params.get('id')
        ).count()

        clientes_cancelados = base_queryset.filter(status='Cancelada').count()

        churm_rate = calculate_churm_rate(clientes_ativos, clientes_cancelados)
        valor_mensal = self.queryset.aggregate(Sum('valor'))
        
        return Response(serializer({
            'churm_rate': churm_rate,
            'clientes_ativos': clientes_ativos,
            'mrr': valor_mensal.get('valor__sum', 0),
            'clientes_cancelados': clientes_cancelados
        }).data)


class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['data_inicio', ]

    def get_queryset(self):
        return self.queryset.filter(planilha__user_dono=self.request.user)
    
    def filter_queryset(self, queryset):
        params = self.request.query_params
        if 'data_inicio' in params:
            datetime_inicio = datetime.fromisoformat(params.get('data_inicio'))
        return queryset.filter(
            data_inicio__year = datetime_inicio.year,
            data_inicio__month = datetime_inicio.month,
            planilha__id = params.get('id')
        )


class PlanilhaViewSet(viewsets.ViewSet):
    queryset = Planilha.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadPlanilhaSerializer
    DATETIME_DICT = {
        'm/d/yy h:mm': '%m/%d/%y %H:%M',
        'mm-dd-yy': '%m/%d/%y',
        'dd/mm/yyyy': '%d/%m/%y',
        'd/mm/yyyy': '%d/%m/%y',
        'dd/m/yyyy': '%d/%m/%y',
        'mm-dd-yy': '%m-%d-%y',
        'General': ''
    }

    def get_queryset(self):
        return self.queryset.filter(user_dono=self.request.user)
    
    
    def list(self, request):
        serializer = PlanilhaSerializer(self.queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request):
        data = request.FILES
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            planilha = Planilha.objects.create(
                nome_planilha = data.get('planilha').name,
                user_dono = request.user
            )

            workbook = load_workbook(data.get('planilha'))
            for worksheet in workbook:
                for row in worksheet.rows:
                    if row[0].row != 1:
                        print(f'data_inicio: {row[2].number_format} | data_status: {row[4].number_format} | data_cancelamento: {row[5].number_format} | proximo_ciclo: {row[7].number_format} | row: {row[0].row}')
                        cobranca = Cobranca()
                        cobranca.quantidade_cobrancas = row[0].value
                        cobranca.frequencia_dias = row[1].value
                        cobranca.data_inicio = cleaned_date(row[2].value)
                        cobranca.status = row[3].value
                        cobranca.data_status = cleaned_date(row[4].value)
                        cobranca.data_cancelamento = cleaned_date(row[5].value)
                        cobranca.valor = row[6].value
                        cobranca.proximo_ciclo = cleaned_date(row[7].value, True)
                        cobranca.id_assinante = row[8].value
                        cobranca.planilha = planilha
                        cobranca.save()
        return Response(status=status.HTTP_201_CREATED)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: MyTokenObtainPairSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class DecoratedTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class DecoratedTokenVerifyView(TokenVerifyView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def cleaned_date(value, date_only=False):
    if isinstance(value, datetime):
        return value
    elif type(value) == str and date_only is False:
        return datetime.strptime(value, '%m/%d/%y %H:%M')
    elif type(value) == str and date_only is True:
        try:
            data = datetime.strptime(value, '%m/%d/%Y')
        except(ValueError):
            data = datetime.strptime(value, '%d/%y/%Y')
        return data
    else:
        return None
    

def calculate_churm_rate(clientes_ativos, clientes_cancelados):
    try:
        return clientes_ativos/clientes_cancelados
    except(ZeroDivisionError):
        return 0