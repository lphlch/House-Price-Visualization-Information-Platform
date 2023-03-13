# Generated by Django 3.2.15 on 2023-03-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20230311_1103'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.RemoveField(
            model_name='neighbourhood',
            name='location',
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='neighbourhood',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]