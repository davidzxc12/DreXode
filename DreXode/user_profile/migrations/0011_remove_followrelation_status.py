# Generated by Django 2.0.1 on 2018-01-10 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_followrelation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followrelation',
            name='status',
        ),
    ]
