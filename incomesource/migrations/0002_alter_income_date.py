# Generated by Django 4.1.2 on 2022-11-08 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomesource', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
