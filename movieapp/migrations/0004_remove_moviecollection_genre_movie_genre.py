# Generated by Django 4.1 on 2022-08-31 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0003_alter_moviecollection_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviecollection',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='horror', max_length=100),
        ),
    ]
