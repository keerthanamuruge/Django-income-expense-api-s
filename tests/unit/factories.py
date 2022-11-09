import factory
from faker import Faker
from authentication.models import User
from expenses.models import Expenses
from incomesource.models import Income

fake = Faker()
from datetime import datetime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name
    email = "user@example.com"
    password = 'user123'


class ExpensesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expenses

    category = "food"
    amount = 123.00
    description = "the description"
    owner = factory.SubFactory(UserFactory)
    date = datetime.now()


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Income

    income = "Business"
    amount = 100000
    description = "description"
    owner = factory.SubFactory(UserFactory)
    date = datetime.now()
