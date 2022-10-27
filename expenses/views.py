from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from .serializers import ExpenseSerializers
from .models import Expenses
from rest_framework import permissions, authentication
from .permissions import IsOwner
from rest_framework.response import Response


class ExpenseListApiView(ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExpenseSerializers
    queryset = Expenses.objects.all()

    def get(self, request):
        return Response({'hello': 1}, 201)

    def post(self, request):
        return Response({'hello': 1}, 201)



    # def perform_create(self, serializer):
    #     return serializer.save(owner=self.request.user)
    #
    # def get_queryset(self):
    #     return self.queryset.filter(owner=self.request.user)


class ExpenseDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
