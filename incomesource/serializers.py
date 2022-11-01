from rest_framework import serializers
from .models import Income


class IncomeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['id', 'income', 'amount', 'description', 'date', 'owner']

