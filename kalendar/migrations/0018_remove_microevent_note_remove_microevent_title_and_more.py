# Generated by Django 4.2.1 on 2023-08-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalendar', '0017_microevent_microevententry_delete_evententry2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microevent',
            name='note',
        ),
        migrations.RemoveField(
            model_name='microevent',
            name='title',
        ),
        migrations.AddField(
            model_name='microevent',
            name='notice',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MicroEventEntry',
        ),
    ]
