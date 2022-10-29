from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.views import APIView
from authentication.models import User
from .serializers import ExpenseSerializers
from .models import Expenses
from rest_framework import permissions, authentication, viewsets, mixins, generics
from .permissions import IsOwner
from rest_framework.response import Response




class ExpenseApiview(generics.GenericAPIView, mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
                     ):
# class ExpenseApiview(APIView):
    queryset = User.objects.all()
    serializer_class = ExpenseSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = 'id'

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)