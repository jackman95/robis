# Generated by Django 4.2.1 on 2023-08-21 14:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kalendar', '0019_microevententry'),
    ]

    operations = [
        migrations.AddField(
            model_name='microevententry',
            name='microevent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kalendar.microevent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='microevententry',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='microevent',
            name='notice',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='microevententry',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='microevententry',
            name='notice',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='microevententry',
            unique_together={('name',)},
        ),
        migrations.RemoveField(
            model_name='microevententry',
            name='micro_event',
        ),
    ]
