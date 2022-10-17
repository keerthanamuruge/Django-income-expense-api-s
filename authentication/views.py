from smtplib import SMTPAuthenticationError

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer, EmailVerification
from rest_framework.response import Response
from .models import User
from .utils import Util
import logging
import jwt

from django.conf import settings

logger = logging.getLogger(__name__)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        user_data['tokens'] = user.tokens()
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        user_email = request.data
        serializer = self.serializer_class(data=user_email)
        user = User.objects.get(email=user_email['email'])
        token = user.tokens()
        response_data={}

        current_site = get_current_site(request).domain
        relative_link = reverse('email_verify')
        absurl = 'http://' + current_site + relative_link + "?token=" + token.get('access_token')
        email_body = 'Hi ' + user.username + ' Please verify your email by click below\n' + absurl
        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user_email['email']}

        try:
            Util.send_email(data=data)
            response_data['message'] = 'success'
        except SMTPAuthenticationError:
            response_data['message'] = 'email is not authenticated'
            logger.exception('not able send email')
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_data, status=status.HTTP_200_OK)


class EmailVerify(views.APIView):
    serializer_class = EmailVerification

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            # auth = JWTAuthentication()
            # auth.authenticate(request)
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.is_verified = True
            user.save()

            return Response({'message': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'message': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
