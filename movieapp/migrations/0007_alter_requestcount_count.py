# Generated by Django 4.1 on 2022-09-01 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0006_requestcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestcount',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
