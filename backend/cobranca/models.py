from django.db import models
from django.contrib.auth.models import User

class Planilha(models.Model):
    nome_planilha = models.CharField(max_length=300)
    data_envio_planilha = models.DateTimeField(auto_now=True)
    user_dono = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Cobranca(models.Model):
    STATUS = [
        ("ativa", "Ativa"),
        ("cancelada", "Cancelada"),
        ("trial cancelado", "Trial cancelado"),
        ("atrasada", "Atrasada"),
        ("upgrade"," Upgrade"),
    ]

    quantidade_cobrancas = models.IntegerField()
    frequencia_dias = models.IntegerField()
    data_inicio = models.DateTimeField()
    status = models.CharField(choices=STATUS, max_length=50, default='ativa')
    data_status = models.DateTimeField()
    data_cancelamento = models.DateTimeField(blank=True, null=True)
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    proximo_ciclo = models.DateField()
    id_assinante = models.CharField(max_length=70)
    planilha = models.ForeignKey(Planilha, on_delete=models.CASCADE)
