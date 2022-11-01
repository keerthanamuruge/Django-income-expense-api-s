from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializers
from .models import Expenses
from rest_framework import permissions


class ExpenseListApiView(ListCreateAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expenses.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expenses.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
