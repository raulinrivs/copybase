from django.db import models

class Artigo(models.Model):
    author = models.CharField(verbose_name='Autor', max_length=200, null=True, blank=True)
    title = models.CharField(verbose_name='Titulo', max_length=200, null=True, blank=True)
    description = models.TextField(verbose_name='Descricao', null=True, blank=True)
