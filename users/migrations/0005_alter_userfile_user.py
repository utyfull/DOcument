# Generated by Django 5.0.6 on 2024-05-14 20:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_sharedwith_userfile_shared_with'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_files', to=settings.AUTH_USER_MODEL),
        ),
    ]
