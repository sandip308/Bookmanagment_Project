# Generated by Django 3.0.3 on 2020-04-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookdata', '0010_auto_20200405_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
