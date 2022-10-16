# Generated by Django 4.1 on 2022-10-11 13:02

import analytics.field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_channel_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='団体名')),
                ('slack_app_token', analytics.field.EncryptedTextField(max_length=100, verbose_name='SlackAppToken')),
            ],
        ),
    ]