# Generated by Django 2.0.1 on 2018-01-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='songs',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]