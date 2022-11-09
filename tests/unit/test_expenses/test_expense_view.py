from collections import OrderedDict
from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestExpenseListApiView:

    def test_get_and_post_with_out_authorization(self, api_client, create_user):
        url = reverse('expenses')
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_get_with_request(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner

        url = reverse('expenses')
        print(user.tokens())
        response = api_client.get(url, HTTP_AUTHORIZATION= f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [OrderedDict(
            [('id', 1), ('category', 'online_services'), ('amount', '123.00'), ('description', 'the description'),
                ('date', ANY)])
        ]

    def test_post_with_request(self, create_user_factory, api_client):
        user = create_user_factory
        url = reverse('expenses')
        print(user.tokens())
        response = api_client.post(url,
                                   {
                                       'category': 'ONLINE_SERVICES',
                                       'amount': 200,
                                       'description': 'description',
                                       'owner': create_user_factory.id
                                   },
                                   HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}",
                                   )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'id': 2, 'category': 'ONLINE_SERVICES', 'amount': '200.00', 'description': 'description', 'date': ANY}


class TestExpenseDetailApiView:

    def test_unauthorization(self, api_client, create_user_factory):
        url = reverse('expense', kwargs={'id': create_user_factory.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.put(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.patch(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_expense_that_not_created(self, api_client, create_user_factory):
        user = create_user_factory
        url = reverse('expense', kwargs={'id': user.id})
        response = api_client.get(url,
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'error': 'No Expenses matches the given query.', 'code': 'No Expenses matches the given query.'}

    def test_get(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner
        url = reverse('expense', kwargs={'id': create_expenses_factory.id})
        response = api_client.get(url,
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': create_expenses_factory.id, 'category': 'online_services', 'amount': '123.00',
                                 'description': 'the description', 'date': ANY}

    def test_put(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner
        url = reverse('expense', kwargs={'id': create_expenses_factory.id})
        response = api_client.put(url,
                                  {
                                      "category": "RENT",
                                      "amount": 12345,
                                      "description": "description",
                                  },
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': create_expenses_factory.id, 'category': 'RENT', 'amount': '12345.00',
                                 'description': 'description', 'date': ANY}

    def test_put_with_wrong_request(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner
        url = reverse('expense', kwargs={'id': create_expenses_factory.id})
        response = api_client.put(url,
                                  {
                                      "category": "rent",
                                      "amount": 12345,
                                      "description": "description",
                                  },
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner
        url = reverse('expense', kwargs={'id': create_expenses_factory.id})
        response = api_client.patch(url,
                                  {
                                      "amount": 4567,
                                      "description": "hello world",
                                  },
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': create_expenses_factory.id, 'category': 'online_services', 'amount': '4567.00',
                                 'description': 'hello world', 'date': ANY}

    def test_delete(self, api_client, create_expenses_factory):
        user = create_expenses_factory.owner
        url = reverse('expense', kwargs={'id': create_expenses_factory.id})
        response = api_client.delete(url, HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

