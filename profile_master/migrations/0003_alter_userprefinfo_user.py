# Generated by Django 4.0.4 on 2022-04-25 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile_master', '0002_alter_userprefinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprefinfo',
            name='User',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
