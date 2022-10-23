# Generated by Django 4.1 on 2022-10-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_base_organization_channel_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='name',
            field=models.CharField(max_length=50, verbose_name='拠点'),
        ),
        migrations.AddConstraint(
            model_name='base',
            constraint=models.UniqueConstraint(fields=('name', 'organization'), name='name_organization_unique'),
        ),
    ]