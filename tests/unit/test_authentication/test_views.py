from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from authentication.models import User
import json
from authentication.views import RegisterView, LoginApiView, VerifyEmail, EmailVerify


class TestRegsiterViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_without_required_request(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            'error':
                {
                    'username': [ErrorDetail(string='This field is required.', code='required')],
                    'password': [ErrorDetail(string='This field is required.', code='required')]
                }
        }

    def test_register_with_correct_request(self):
        response = self.client.post(self.url, {
            "username": "keerthana",
            "password": "Keerthu2001",
            "email": "keerthuofficial2001@softsuave.com"
        }
                                    )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': 1,
            'username': 'keerthana', 'email': 'keerthuofficial2001@softsuave.com', 'tokens': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3ODU5MDQ4LCJpYXQiOjE2Njc2NDMwNDgsImp0aSI6IjIyMjhjMzk1MWZmMzQxMDc4MGYzNmQxYmQ1ZDU1OTk5IiwidXNlcl9pZCI6MX0.Bn8r--MHEpr0ak2nBjpSOU4X66cL08MjJy7B-IYX_AI',
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NzcyOTQ0OCwiaWF0IjoxNjY3NjQzMDQ4LCJqdGkiOiIwYWNjMDU1NzM2OTY0NTM2YmUxZjgyZTUzMzZjZGFmZSIsInVzZXJfaWQiOjF9.wBFWuI1IWUgQOA_FIPET-M84C61KT8QMJeapNM38GPk'
                }
            }
