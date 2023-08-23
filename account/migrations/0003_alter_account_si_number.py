# Generated by Django 4.2.1 on 2023-08-20 11:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_si_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='si_number',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(8999999), django.core.validators.MinValueValidator(1000)], verbose_name='Číslo čipu'),
        ),
    ]