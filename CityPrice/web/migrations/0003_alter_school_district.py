# Generated by Django 3.2.15 on 2023-03-10 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_park_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.district'),
        ),
    ]