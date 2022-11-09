from django.db import models

from authentication.models import User


class Income(models.Model):
    SOURCE_OF_INCOME = [
        ('BUSINESS', 'BUSINESS'),
        ('TRAVEL', 'TRAVEL'),
        ('SE', 'SE'),
        ('HOME_RENT', 'HOME_RENT'),
        ('OTHERS', 'OTHERS'),
    ]

    income = models.CharField(choices=SOURCE_OF_INCOME, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, auto_now_add=True)