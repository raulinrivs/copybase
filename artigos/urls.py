from django.urls import path
from artigos.views import ArtigoAPIView

urlpatterns = [
    path('artigos/', ArtigoAPIView.as_view(), name='api-artigos'),
]
