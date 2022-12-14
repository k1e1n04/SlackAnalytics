# Generated by Django 4.0.4 on 2022-06-18 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_channel_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='拠点'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='channel_id',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='チャンネルID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='slack_id',
            field=models.CharField(max_length=30, unique=True, verbose_name='SlackID'),
        ),
    ]
