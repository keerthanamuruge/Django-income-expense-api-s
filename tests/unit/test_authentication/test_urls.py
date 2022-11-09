from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import RegisterView, LoginApiView, VerifyEmail, EmailVerify


class TestAuthUrls(SimpleTestCase):

    def test_register_urls(self):
        url = reverse('register')
        assert resolve(url).func.cls == RegisterView

    def test_login_url(self):
        url = reverse('login')
        assert resolve(url).func.cls == LoginApiView

    def test_verify_email_url(self):
        url = reverse('verify_email')
        assert resolve(url).func.cls == VerifyEmail

    def test_EmailVerify_url(self):
        url = reverse('email_verify')
        assert resolve(url).func.cls == EmailVerify

    def test_EmailVerify_url(self):
        url = reverse('token_refresh')
        assert resolve(url).func.cls == TokenRefreshView