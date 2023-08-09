from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

client = Client()

class GetArtigos(TestCase):

    def test_get_artigoss(self):
        response = client.get(reverse('api-artigos'))
        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        