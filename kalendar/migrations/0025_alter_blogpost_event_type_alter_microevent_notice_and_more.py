# Generated by Django 4.2.1 on 2023-08-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalendar', '0024_alter_blogpost_contact_alter_blogpost_discipline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='event_type',
            field=models.CharField(choices=[('trenink', 'Trénink'), ('tc-oddil', 'Oddílové soustředění'), ('3st', 'soutěž III. stupně'), ('2st', 'soutěž II. stupně'), ('ostatni', 'Ostatní'), ('mcr-nz', 'MČR/NŽ - I. stupeň'), ('repre', 'Reprezentační akce'), ('zdr', 'ŽDR akce')], max_length=30),
        ),
        migrations.AlterField(
            model_name='microevent',
            name='notice',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='microevententry',
            name='notice_name',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
