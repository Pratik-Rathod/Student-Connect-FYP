# Generated by Django 4.0.4 on 2022-04-24 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_delete_postcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='cover_img',
            field=models.ImageField(null=True, upload_to='img/'),
        ),
    ]
