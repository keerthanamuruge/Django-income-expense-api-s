from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginApiView, VerifyEmail, EmailVerify

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('verify_email/', VerifyEmail.as_view(), name='verify_email'),
    path('email_verify/', EmailVerify.as_view(), name='email_verify'),
    path('reclaim/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
