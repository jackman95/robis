# Generated by Django 4.2.1 on 2023-08-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalendar', '0025_alter_blogpost_event_type_alter_microevent_notice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='microevent',
            name='max_entries',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='event_type',
            field=models.CharField(choices=[('trenink', 'Trénink'), ('tc-oddil', 'Oddílové soustředění'), ('3st', 'Soutěž III. stupně'), ('2st', 'Soutěž II. stupně'), ('ostatni', 'Ostatní'), ('mcr-nz', 'MČR/NŽ - I. stupeň'), ('repre', 'Reprezentační akce'), ('zdr', 'ŽDR akce')], max_length=30),
        ),
    ]
