# Generated by Django 4.2.4 on 2024-03-22 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Planilha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_planilha', models.CharField(max_length=300)),
                ('data_envio_planilha', models.DateTimeField(auto_now_add=True)),
                ('user_dono', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cobranca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_cobrancas', models.IntegerField()),
                ('frequencia_dias', models.IntegerField()),
                ('data_inicio', models.DateTimeField()),
                ('status', models.CharField(choices=[('ativa', 'Ativa'), ('cancelada', 'Cancelada')], default='ativa', max_length=50)),
                ('data_status', models.DateTimeField()),
                ('data_cancelamento', models.DateTimeField(blank=True, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proximo_ciclo', models.DateField()),
                ('id_assinante', models.CharField(max_length=70)),
                ('planilha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cobranca.planilha')),
            ],
        ),
    ]
