# Generated by Django 2.0.1 on 2018-01-25 14:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0004_auto_20180125_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(default='', on_delete=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
