import pytest
from rest_framework.test import APIClient
from faker import Faker
from authentication.models import User
from tests.unit.factories import IncomeFactory
from pytest_factoryboy import register
from .factories import UserFactory, ExpensesFactory

fake = Faker()
register(UserFactory)
register(ExpensesFactory)
register(IncomeFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    user_name = fake.name()
    email = fake.email()
    password = fake.password()
    User.objects.create_user(**{"username": user_name, "email": email, "password": password
        })
    return (User.objects.get(email=email), password)


@pytest.fixture
def create_user_factory(user_factory):
    return user_factory.create()


@pytest.fixture
def create_expenses_factory(create_user_factory, expenses_factory):
    return expenses_factory(category='online_services', owner=create_user_factory)


@pytest.fixture
def create_income_factory(user_factory, income_factory):
    user = user_factory(email=fake.email())
    return income_factory(owner=user)


@pytest.fixture
def extra_user(user_factory):
    return user_factory(email=fake.email())