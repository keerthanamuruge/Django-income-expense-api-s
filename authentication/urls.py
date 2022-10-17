from django.urls import path

from .views import RegisterView, LoginApiView, VerifyEmail, EmailVerify

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('verify_email/', VerifyEmail.as_view(), name='verify_email'),
    path('email_verify/', EmailVerify.as_view(), name='email_verify'),
]
