from django.test import TestCase
from authentication.models import User

class TestUserModel(TestCase):
    def setUp(self):
        User.objects.create_user(username="income", password="Income12", email="incom@gmail.com")

    def test_create_user_model(self):

        income = User.objects.get(email="incom@gmail.com")
        assert income.username == "income"