# Generated by Django 4.2.1 on 2023-08-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='index',
            field=models.CharField(blank=True, max_length=7, null=True, unique=True, verbose_name='Index'),
        ),
    ]
