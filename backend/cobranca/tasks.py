# from datetime import date
# from celery import shared_task
# from cobranca.models import Reserva
# from django.core.mail import send_mail
# from config.celery import app


# @shared_task
# def enviarEmailAsync(titulo, mensagem, enviado_de, enviado_para):
#     print(titulo, mensagem, enviado_de, enviado_para)
#     send_mail(titulo, mensagem, enviado_de, [enviado_para])


# @shared_task
# def liberarQuartosCheckOutCancelamento():
#     reservas = Reserva.objects.filter(ativo=False, data_inicio=date.today().isoformat(), quarto__reservado=True)
#     for reserva in reservas:
#         reserva.quarto.reservado = False
#         reserva.quarto.save()
