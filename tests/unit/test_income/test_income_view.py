from collections import OrderedDict
from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestIncomeListApiView:

    def test_get_and_post_with_out_authorization(self, api_client, create_user):
        url = reverse('income')
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_get_with_request(self, api_client, create_income_factory):
        user = create_income_factory.owner

        url = reverse('income')
        print(user.tokens())
        response = api_client.get(url, HTTP_AUTHORIZATION= f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [OrderedDict([('id', 1), ('income', 'Business'), ('amount', '100000.00'), ('description', 'description'), ('date', ANY), ('owner', user.id)])]

    def test_post_with_request(self, create_user_factory, api_client):
        user = create_user_factory
        url = reverse('income')
        print(user.tokens())
        response = api_client.post(url,
                                   {
                                       'income': 'TRAVEL',
                                       'amount': 200,
                                       'description': 'description',
                                       'owner': create_user_factory.id
                                   },
                                   HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}",
                                   )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'id': 2, 'income': 'TRAVEL', 'amount': '200.00', 'description': 'description', 'date':
        ANY, 'owner': user.id}

    def test_post_with_wrong_owner_id(self, create_user_factory, api_client):
        user = create_user_factory
        url = reverse('income')
        print(user.tokens())
        response = api_client.post(url,
                                   {
                                       'income': 'TRAVEL',
                                       'amount': 200,
                                       'description': 'description',
                                       'owner': 5
                                   },
                                   HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}",
                                   )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

class TestIncomeDetailApiView:


    def test_unauthorization(self, api_client, create_user_factory):
        income_detail_url = reverse('income_detail', args={create_user_factory.id})
        response = api_client.get(income_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.put(income_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = api_client.delete(income_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_income_that_not_created(self, api_client, create_user_factory):
        user = create_user_factory
        income_detail_url_1 = reverse('income_detail', args={user.id})
        response = api_client.get(income_detail_url_1,
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'error': 'No Income matches the given query.', 'code': 'No Income matches the given query.'}

    def test_get(self, api_client, extra_user,income_factory):
        user = extra_user
        income_source = income_factory(owner=user)
        income_detail_url_2 = reverse('income_detail', args={income_source.id})
        response = api_client.get(income_detail_url_2,
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': income_source.id, 'income': 'Business', 'amount': '100000.00', 'description': 'description',
                                 'date': ANY, 'owner': user.id}

    def test_put(self, api_client, extra_user, income_factory):
        user = extra_user
        income_source = income_factory(owner=user)
        income_detail_url_3 = reverse('income_detail', args={income_source.id})
        response = api_client.put(income_detail_url_3,
                                  {
                                      "income": "TRAVEL",
                                      "amount": 12345,
                                      "description": "description",
                                      "owner": user.id,
                                  },
                                  HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'id': income_source.id, 'income': 'TRAVEL', 'amount': '12345.00', 'description': 'description',
                                 "date": ANY, 'owner': user.id}

    def test_delete(self, api_client, create_income_factory):
        user = create_income_factory.owner
        income_detail_url4 = reverse('income_detail', args={create_income_factory.id})
        response = api_client.delete(income_detail_url4, HTTP_AUTHORIZATION=f"Bearer {user.tokens().get('access_token')}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

