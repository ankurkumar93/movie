# Generated by Django 4.1 on 2022-09-01 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0005_alter_moviecollection_movies'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
        ),
    ]
