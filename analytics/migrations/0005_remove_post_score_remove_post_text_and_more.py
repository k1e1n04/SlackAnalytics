# Generated by Django 4.0.4 on 2022-07-07 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_post_base'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='score',
        ),
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AlterField(
            model_name='post',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.employee', verbose_name='メンバー'),
        ),
    ]
