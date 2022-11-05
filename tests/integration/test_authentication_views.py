from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from authentication.models import User
import json
from authentication.views import RegisterView, LoginApiView, VerifyEmail, EmailVerify

pytestmark = pytest.mark.django_db


class TestRegsiterViews:

    def test_register_without_required_request(self, api_client):
        url = reverse('register')
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'error':
                                     {'username': [ErrorDetail(string='This field is required.', code='required')],
                                      'email': [ErrorDetail(string='This field is required.', code='required')],
                                      'password': [ErrorDetail(string='This field is required.', code='required')]
                                      }, 'code': 'invalid'
                                 }

    def test_register_with_correct_request(self, api_client):
        url = reverse('register')
        response = api_client.post(url, {
            "username": "keerthana",
            "password": "Keerthu2001",
            "email": "keerthuofficial2001@softsuave.com"
            })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            'id': 1,
            'username': 'keerthana', 'email': 'keerthuofficial2001@softsuave.com', 'tokens': {
                'access_token': ANY,
                'refresh_token': ANY
                }
            }

